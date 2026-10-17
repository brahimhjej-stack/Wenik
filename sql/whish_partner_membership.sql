-- Apply after whish_statement_checkout.sql. No production deployment yet.
begin;
create table public.whish_statement_memberships (
 statement_id uuid primary key references public.partner_monthly_statements(id),
 order_id uuid not null unique references public.whish_checkout_orders(id),
 partner_id uuid not null references public.partners(id),
 starts_at timestamptz not null,
 ends_at timestamptz not null check(ends_at>starts_at),
 created_at timestamptz not null default now()
);
alter table public.whish_statement_memberships enable row level security;
revoke all on public.whish_statement_memberships from public,anon,authenticated;
grant all on public.whish_statement_memberships to service_role;

alter function public.whish_reconcile_order(uuid,text,text) rename to whish_reconcile_statement_ledger;
create function public.whish_reconcile_order(p_order uuid,p_environment text,p_state text)
returns jsonb language plpgsql security invoker set search_path='' as $$
declare result jsonb; o public.whish_checkout_orders; s public.partner_monthly_statements;
 sub public.partner_subscriptions; start_at timestamptz; end_at timestamptz;
begin
 result:=public.whish_reconcile_statement_ledger(p_order,p_environment,p_state);
 if p_environment<>'production' or p_state<>'success' then return result; end if;
 select * into o from public.whish_checkout_orders where id=p_order and environment='production';
 if o.kind<>'partner' or o.statement_id is null or o.fulfilled_at is null or o.state<>'success' then return result; end if;
 select * into s from public.partner_monthly_statements where id=o.statement_id for update;
 -- A commission-only invoice (including the free trial) never buys a month.
 if s.status<>'paid' or s.paid_amount<s.total_due or s.monthly_subscription<=0 then return result; end if;
 if exists(select 1 from public.whish_statement_memberships where statement_id=s.id) then return result; end if;
 insert into public.partner_subscriptions(partner_id,trial_started_at,trial_ends_at)
 select p.id,p.created_at,p.created_at+make_interval(months=>cfg.partner_trial_months)
 from public.partners p cross join public.whish_checkout_settings cfg where p.id=s.partner_id and cfg.id=true
 on conflict(partner_id) do nothing;
 select * into sub from public.partner_subscriptions where partner_id=s.partner_id for update;
 if sub.id is null then raise exception 'SUBSCRIPTION_NOT_FOUND'; end if;
 start_at:=greatest(now(),sub.trial_ends_at,coalesce(sub.paid_until,sub.trial_ends_at));
 end_at:=start_at+interval '1 month';
 insert into public.whish_statement_memberships(statement_id,order_id,partner_id,starts_at,ends_at)
 values(s.id,o.id,s.partner_id,start_at,end_at);
 -- Payment never overrides an administrative suspension.
 update public.partner_subscriptions set paid_until=end_at,
 status=case when status='suspended' then status else 'active' end,
 preferred_payment_method='whish',updated_at=now() where id=sub.id;
 return result||jsonb_build_object('membershipPaidUntil',end_at);
end $$;
revoke all on function public.whish_reconcile_statement_ledger(uuid,text,text),public.whish_reconcile_order(uuid,text,text) from public,anon,authenticated;
grant execute on function public.whish_reconcile_statement_ledger(uuid,text,text),public.whish_reconcile_order(uuid,text,text) to service_role;
commit;
