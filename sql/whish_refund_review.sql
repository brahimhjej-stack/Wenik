-- Record verified refunds for explicit Super Admin review, not an API refund request.
begin;
create table public.whish_refund_reviews (
 order_id uuid primary key references public.whish_checkout_orders(id),
 status text not null default 'open' check(status in ('open','resolved')),
 resolution text check(resolution in ('keep_access','set_paid_until')),
 note text,
 opened_at timestamptz not null default now(),
 resolved_at timestamptz,
 resolved_by uuid references auth.users(id)
);
alter table public.whish_refund_reviews enable row level security;
revoke all on public.whish_refund_reviews from public,anon,authenticated;
grant all on public.whish_refund_reviews to service_role;

alter function public.whish_reconcile_order(uuid,text,text) rename to whish_reconcile_membership;
create function public.whish_reconcile_order(p_order uuid,p_environment text,p_state text)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare o public.whish_checkout_orders; result jsonb;
begin
 if p_state is null or p_state not in ('pending','success','failed','refunded','unknown') then raise exception 'INVALID_STATE'; end if;
 select * into o from public.whish_checkout_orders where id=p_order and environment=p_environment for update;
 if o.id is null then raise exception 'ORDER_NOT_FOUND'; end if;
 -- A delayed success must never erase a previously verified refund.
 if o.state='refunded' then
  result:=jsonb_build_object('state','refunded','sandbox',p_environment='sandbox');
 else
  result:=public.whish_reconcile_membership(p_order,p_environment,p_state);
 end if;
 if result->>'state'='refunded' then
  insert into public.whish_refund_reviews(order_id) values(o.id) on conflict(order_id) do nothing;
  result:=result||jsonb_build_object('reviewRequired',(select status='open' from public.whish_refund_reviews where order_id=o.id));
 end if;
 return result;
end $$;
revoke all on function public.whish_reconcile_membership(uuid,text,text),public.whish_reconcile_order(uuid,text,text) from public,anon,authenticated;
grant execute on function public.whish_reconcile_membership(uuid,text,text),public.whish_reconcile_order(uuid,text,text) to service_role;

create function public.whish_admin_refund_reviews() returns jsonb
language plpgsql security definer set search_path='' as $$
declare result jsonb;
begin
 if auth.uid() is null or not public.is_wenik_super_admin() then raise exception 'NOT_AUTHORIZED'; end if;
 select coalesce(jsonb_agg(to_jsonb(x)),'[]'::jsonb) into result from (
  select r.order_id,r.status,r.resolution,r.note,r.opened_at,o.kind,o.amount,o.currency,o.environment,o.invoice_no,
  case when o.kind='customer' then (select paid_until from public.whish_customer_memberships where customer_id=o.subject_id)
  else (select paid_until from public.partner_subscriptions where partner_id=o.subject_id) end as paid_until
  from public.whish_refund_reviews r join public.whish_checkout_orders o on o.id=r.order_id
  order by r.opened_at desc limit 100
 ) x;
 return result;
end $$;

create function public.whish_resolve_refund_review(p_order uuid,p_resolution text,p_note text,p_paid_until timestamptz default null)
returns void language plpgsql security definer set search_path='' as $$
declare o public.whish_checkout_orders; r public.whish_refund_reviews; before_end timestamptz;
begin
 if auth.uid() is null or not public.is_wenik_super_admin() then raise exception 'NOT_AUTHORIZED'; end if;
 if p_resolution is null or p_resolution not in ('keep_access','set_paid_until') or p_note is null or length(trim(p_note))<5 or length(p_note)>2000 then raise exception 'INVALID_REVIEW'; end if;
 select * into o from public.whish_checkout_orders where id=p_order for update;
 select * into r from public.whish_refund_reviews where order_id=p_order for update;
 if r.order_id is null or r.status<>'open' then raise exception 'REVIEW_NOT_OPEN'; end if;
 if o.state<>'refunded' then raise exception 'REFUND_NOT_VERIFIED'; end if;
 if p_resolution='set_paid_until' then
  if o.environment<>'production' or p_paid_until is null then raise exception 'INVALID_EXPIRY_CHANGE'; end if;
  if o.kind='customer' then
   select paid_until into before_end from public.whish_customer_memberships where customer_id=o.subject_id for update;
   if not found then raise exception 'MEMBERSHIP_NOT_FOUND'; end if;
   update public.whish_customer_memberships set paid_until=p_paid_until,updated_at=now() where customer_id=o.subject_id;
  else
   select paid_until into before_end from public.partner_subscriptions where partner_id=o.subject_id for update;
   if not found then raise exception 'MEMBERSHIP_NOT_FOUND'; end if;
   update public.partner_subscriptions set paid_until=p_paid_until,updated_at=now() where partner_id=o.subject_id;
  end if;
 end if;
 update public.whish_refund_reviews set status='resolved',resolution=p_resolution,note=trim(p_note),resolved_at=now(),resolved_by=auth.uid() where order_id=p_order;
 insert into public.audit_logs(actor_auth_user_id,actor_role,action,entity_type,entity_id,payload)
 values(auth.uid(),'super_admin','whish_refund_reviewed','whish_checkout_order',p_order::text,jsonb_build_object('resolution',p_resolution,'note',trim(p_note),'previous_paid_until',before_end,'new_paid_until',p_paid_until));
end $$;
revoke all on function public.whish_admin_refund_reviews(),public.whish_resolve_refund_review(uuid,text,text,timestamptz) from public,anon;
grant execute on function public.whish_admin_refund_reviews(),public.whish_resolve_refund_review(uuid,text,text,timestamptz) to authenticated;
commit;
