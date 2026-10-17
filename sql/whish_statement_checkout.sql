-- Apply after whish_checkout.sql in the test database first.
begin;
alter table public.whish_checkout_orders add column statement_id uuid references public.partner_monthly_statements(id);
alter table public.whish_checkout_orders add column invoice_no text;
create index whish_orders_statement on public.whish_checkout_orders(statement_id,environment);
alter table public.partner_statement_payments add column whish_order_id uuid unique references public.whish_checkout_orders(id);

create function public.whish_prepare_statement_order(p_user uuid,p_statement uuid,p_environment text)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare s public.partner_monthly_statements; o public.whish_checkout_orders; remaining numeric;
begin
 if p_user is null or p_statement is null or p_environment not in ('sandbox','production') then raise exception 'INVALID_REQUEST'; end if;
 if not (select enabled from public.whish_checkout_settings where id=true) then raise exception 'CHECKOUT_DISABLED'; end if;
 if not exists(select 1 from public.billing_settings where id=true) then raise exception 'BILLING_SETTINGS_MISSING'; end if;
 if (select currency from public.billing_settings where id=true)<>'USD' then raise exception 'UNSUPPORTED_CURRENCY'; end if;
 select * into s from public.partner_monthly_statements where id=p_statement;
 if s.id is null or s.status='void' then raise exception 'STATEMENT_NOT_PAYABLE'; end if;
 if not exists(select 1 from public.partner_users u join public.partners p on p.id=u.partner_id where u.partner_id=s.partner_id and u.auth_user_id=p_user and u.is_active and u.role::text='partner_manager' and p.status='active') then raise exception 'NOT_AUTHORIZED'; end if;
 perform pg_advisory_xact_lock(hashtextextended('statement'||p_statement::text||p_environment,0));
 select * into s from public.partner_monthly_statements where id=p_statement for update;
 -- Sandbox confirmations do not touch the real ledger, but still must not
 -- issue another test charge for an already confirmed statement.
 if p_environment='sandbox' then
  select * into o from public.whish_checkout_orders where statement_id=p_statement and environment=p_environment and state='success' and fulfilled_at is not null order by created_at desc limit 1;
  if o.id is not null then return to_jsonb(o); end if;
 end if;
 remaining:=greatest(s.total_due-s.paid_amount,0);
 if remaining<1 then raise exception 'NO_PAYABLE_BALANCE'; end if;
 select * into o from public.whish_checkout_orders where statement_id=p_statement and environment=p_environment and state in ('pending','unknown') order by created_at desc limit 1;
 -- A payable link keeps its quoted amount. Resolve it before issuing another link.
 if o.id is null then
  insert into public.whish_checkout_orders(auth_user_id,kind,subject_id,statement_id,invoice_no,environment,amount) values(p_user,'partner',s.partner_id,s.id,s.invoice_no,p_environment,remaining) returning * into o;
 elsif o.auth_user_id<>p_user then raise exception 'STATEMENT_PAYMENT_IN_PROGRESS'; end if;
 return to_jsonb(o);
end $$;
revoke all on function public.whish_prepare_statement_order(uuid,uuid,text) from public,anon,authenticated;
grant execute on function public.whish_prepare_statement_order(uuid,uuid,text) to service_role;

-- Wrap the subscription reconciler so partner payments settle the invoice once.
alter function public.whish_reconcile_order(uuid,text,text) rename to whish_reconcile_subscription_order;
create function public.whish_reconcile_order(p_order uuid,p_environment text,p_state text)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare o public.whish_checkout_orders;
begin
 if p_state not in ('pending','success','failed','refunded','unknown') then raise exception 'INVALID_STATE'; end if;
 select * into o from public.whish_checkout_orders where id=p_order and environment=p_environment for update;
 if o.id is null then raise exception 'ORDER_NOT_FOUND'; end if;
 if o.statement_id is null then
  if o.kind='partner' then raise exception 'PARTNER_STATEMENT_REQUIRED'; end if;
  return public.whish_reconcile_subscription_order(p_order,p_environment,p_state);
 end if;
 perform pg_advisory_xact_lock(hashtextextended('statement'||o.statement_id::text||p_environment,0));
 if o.fulfilled_at is not null and p_state not in ('success','refunded') then return jsonb_build_object('state',o.state); end if;
 if p_state='success' and o.fulfilled_at is null then
  if p_environment='production' then
   insert into public.partner_statement_payments(statement_id,amount,currency,payment_method,provider_reference,whish_order_id,note) values(o.statement_id,o.amount,o.currency,'whish',o.id::text,o.id,'Verified Whish payment') on conflict(whish_order_id) do nothing;
   perform public.refresh_partner_statement_totals(o.statement_id);
  end if;
  update public.whish_checkout_orders set fulfilled_at=now() where id=o.id;
 end if;
 update public.whish_checkout_orders set state=p_state,checked_at=now() where id=o.id;
 return jsonb_build_object('state',p_state,'sandbox',p_environment='sandbox','statementId',o.statement_id);
end $$;
revoke all on function public.whish_reconcile_order(uuid,text,text) from public,anon,authenticated;
grant execute on function public.whish_reconcile_order(uuid,text,text) to service_role;
create trigger whish_guard_statement_adjustments before insert or update or delete on public.partner_statement_adjustments for each row execute function public.whish_guard_billing_write();
commit;
