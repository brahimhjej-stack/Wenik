-- Reviewed setup script for Whish checkout. Apply in a test database first.
begin;
create table public.whish_checkout_settings (
 id boolean primary key default true check(id),
 enabled boolean not null default false,
 partner_trial_months integer not null default 3 check(partner_trial_months between 0 and 12),
 updated_at timestamptz not null default now()
);
insert into public.whish_checkout_settings(id) values(true);
create table public.whish_checkout_orders (
 id uuid primary key default gen_random_uuid(),
 auth_user_id uuid not null references auth.users(id),
 kind text not null check(kind in ('customer','partner')),
 subject_id uuid not null,
 environment text not null check(environment in ('sandbox','production')),
 amount numeric(12,2) not null check(amount>=1),
 currency text not null default 'USD' check(currency='USD'),
 state text not null default 'pending' check(state in ('pending','success','failed','refunded','unknown')),
 collect_url text,
 fulfilled_at timestamptz,
 created_at timestamptz not null default now(),
 checked_at timestamptz
);
create index whish_orders_subject on public.whish_checkout_orders(kind,subject_id,environment,created_at desc);
create table public.whish_customer_memberships (
 customer_id uuid primary key references public.customers(id),
 paid_until timestamptz not null,
 updated_at timestamptz not null default now()
);
alter table public.whish_checkout_settings enable row level security;
alter table public.whish_checkout_orders enable row level security;
alter table public.whish_customer_memberships enable row level security;
revoke all on public.whish_checkout_settings,public.whish_checkout_orders,public.whish_customer_memberships from public,anon,authenticated;
grant all on public.whish_checkout_settings,public.whish_checkout_orders,public.whish_customer_memberships to service_role;

-- Only the active super admin may change fees or switch checkout availability.
-- A future price change applies to new orders, never to an existing quoted order.
create function public.whish_update_settings(p_customer_fee numeric,p_partner_fee numeric,p_enabled boolean,p_trial_months integer)
returns void language plpgsql security definer set search_path='' as $$
begin
 if auth.uid() is null or not public.is_wenik_super_admin() then raise exception 'NOT_AUTHORIZED'; end if;
 if p_customer_fee is null or p_partner_fee is null or p_customer_fee<1 or p_partner_fee<1 or p_customer_fee>10000 or p_partner_fee>10000 or p_customer_fee<>round(p_customer_fee,2) or p_partner_fee<>round(p_partner_fee,2) or p_trial_months is null or p_trial_months not between 0 and 12 or p_enabled is null then raise exception 'INVALID_SETTINGS'; end if;
 update public.billing_settings set customer_monthly_fee=p_customer_fee,partner_monthly_fee=p_partner_fee,updated_by=auth.uid(),updated_at=now() where id=true;
 update public.whish_checkout_settings set enabled=p_enabled,partner_trial_months=p_trial_months,updated_at=now() where id=true;
 insert into public.audit_logs(actor_auth_user_id,actor_role,action,entity_type,entity_id,payload) values(auth.uid(),'super_admin','whish_settings_changed','billing_settings','true',jsonb_build_object('customer_fee',p_customer_fee,'partner_fee',p_partner_fee,'enabled',p_enabled,'trial_months',p_trial_months));
end $$;
revoke all on function public.whish_update_settings(numeric,numeric,boolean,integer) from public,anon;
grant execute on function public.whish_update_settings(numeric,numeric,boolean,integer) to authenticated;

create function public.whish_admin_settings() returns jsonb language plpgsql security definer set search_path='' as $$
declare result jsonb;
begin
 if auth.uid() is null or not public.is_wenik_super_admin() then raise exception 'NOT_AUTHORIZED'; end if;
 select to_jsonb(s) into result from public.whish_checkout_settings s where id=true;
 return result;
end $$;
revoke all on function public.whish_admin_settings() from public,anon;
grant execute on function public.whish_admin_settings() to authenticated;

-- Service role only: caller first validates the bearer token with Supabase Auth.
create function public.whish_prepare_order(p_user uuid,p_kind text,p_environment text)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare s public.whish_checkout_settings; b public.billing_settings; subject uuid; trial_end timestamptz; o public.whish_checkout_orders;
begin
 if p_environment not in ('sandbox','production') or p_kind not in ('customer','partner') or p_user is null then raise exception 'INVALID_REQUEST'; end if;
 select * into s from public.whish_checkout_settings where id=true;
 if not found or not s.enabled then raise exception 'CHECKOUT_DISABLED'; end if;
 select * into b from public.billing_settings where id=true;
 if not found then raise exception 'BILLING_SETTINGS_MISSING'; end if;
 if b.currency<>'USD' then raise exception 'UNSUPPORTED_CURRENCY'; end if;
 if p_kind='customer' then
  select id into subject from public.customers where auth_user_id=p_user and status='active';
 else
  select pu.partner_id into subject from public.partner_users pu join public.partners p on p.id=pu.partner_id where pu.auth_user_id=p_user and pu.is_active and p.status='active' and pu.role::text='partner_manager';
 end if;
 if subject is null then raise exception 'NOT_AUTHORIZED'; end if;
 perform pg_advisory_xact_lock(hashtextextended(p_kind||subject::text||p_environment,0));
 if p_kind='partner' then
  insert into public.partner_subscriptions(partner_id,trial_started_at,trial_ends_at) select subject,p.created_at,p.created_at+make_interval(months=>s.partner_trial_months) from public.partners p where p.id=subject on conflict(partner_id) do nothing;
  select trial_ends_at into trial_end from public.partner_subscriptions where partner_id=subject;
  if trial_end>now() then return jsonb_build_object('trial',true,'trialEndsAt',trial_end); end if;
 end if;
 select * into o from public.whish_checkout_orders where subject_id=subject and kind=p_kind and environment=p_environment and state in ('pending','unknown') order by created_at desc limit 1;
 if o.id is null then
  insert into public.whish_checkout_orders(auth_user_id,kind,subject_id,environment,amount) values(p_user,p_kind,subject,p_environment,case when p_kind='customer' then b.customer_monthly_fee else b.partner_monthly_fee end) returning * into o;
 end if;
 return to_jsonb(o);
end $$;

-- The server must verify Whish's status, never a browser redirect or callback label.
create function public.whish_reconcile_order(p_order uuid,p_environment text,p_state text)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare o public.whish_checkout_orders; next_end timestamptz;
begin
 if p_state not in ('pending','success','failed','refunded','unknown') then raise exception 'INVALID_STATE'; end if;
 select * into o from public.whish_checkout_orders where id=p_order and environment=p_environment for update;
 if o.id is null then raise exception 'ORDER_NOT_FOUND'; end if;
 perform pg_advisory_xact_lock(hashtextextended(o.kind||o.subject_id::text||p_environment,0));
 -- Never regress a paid order on an out-of-order callback.
 if o.fulfilled_at is not null and p_state not in ('success','refunded') then return jsonb_build_object('state',o.state); end if;
 if p_state='success' and o.fulfilled_at is null then
  if p_environment='production' then
   if o.kind='customer' then
    insert into public.whish_customer_memberships(customer_id,paid_until) values(o.subject_id,now()+interval '1 month') on conflict(customer_id) do update set paid_until=greatest(public.whish_customer_memberships.paid_until,now())+interval '1 month',updated_at=now();
   else
    update public.partner_subscriptions set paid_until=greatest(coalesce(paid_until,now()),now())+interval '1 month',updated_at=now() where partner_id=o.subject_id;
    if not found then raise exception 'SUBSCRIPTION_NOT_FOUND'; end if;
   end if;
  end if;
  update public.whish_checkout_orders set fulfilled_at=now() where id=o.id;
 end if;
 update public.whish_checkout_orders set state=p_state,checked_at=now() where id=o.id;
 -- Refunded orders are recorded, never renewed here; entitlement reversal needs review.
 return jsonb_build_object('state',p_state,'sandbox',p_environment='sandbox');
end $$;
revoke all on function public.whish_prepare_order(uuid,text,text),public.whish_reconcile_order(uuid,text,text) from public,anon,authenticated;
grant execute on function public.whish_prepare_order(uuid,text,text),public.whish_reconcile_order(uuid,text,text) to service_role;
-- Enforce super-admin-only edits even through older SECURITY DEFINER billing RPCs.
create function public.whish_guard_billing_write() returns trigger language plpgsql security invoker set search_path='' as $$
begin
 if auth.role()='service_role' or (auth.uid() is null and session_user in ('postgres','supabase_admin')) then
  if tg_op='DELETE' then return old; else return new; end if;
 end if;
 if auth.uid() is null or not public.is_wenik_super_admin() then raise exception 'NOT_AUTHORIZED'; end if;
 if tg_op='DELETE' then return old; else return new; end if;
end $$;
revoke all on function public.whish_guard_billing_write() from public,anon,authenticated;
create trigger whish_guard_settings before update or delete on public.billing_settings for each row execute function public.whish_guard_billing_write();
create trigger whish_guard_partner_payments before insert or update or delete on public.partner_payments for each row execute function public.whish_guard_billing_write();
create trigger whish_guard_statement_payments before insert or update or delete on public.partner_statement_payments for each row execute function public.whish_guard_billing_write();
commit;
