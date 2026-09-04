-- WENIK Finance P&L — SAFE PREVIEW MIGRATION
-- Prepared on staging only. DO NOT apply to production until reviewed/tested.
-- Gifts and customer cashback balances are intentionally excluded from operating P&L.
-- Confirmed partner subscription payments are included automatically as WENIK revenue.

begin;

create table if not exists public.finance_transactions (
  id uuid primary key default gen_random_uuid(),
  occurred_at timestamptz not null default now(),
  entry_type text not null check (entry_type in ('revenue','expense')),
  category text not null,
  amount numeric(14,2) not null check (amount >= 0),
  currency text not null default 'USD',
  partner_id uuid null references public.partners(id) on delete set null,
  source_type text null,
  source_id uuid null,
  notes text null,
  created_by uuid null default auth.uid(),
  created_at timestamptz not null default now(),
  constraint finance_transactions_currency_nonempty check (length(trim(currency)) > 0),
  constraint finance_transactions_category_nonempty check (length(trim(category)) > 0)
);

create index if not exists finance_transactions_occurred_at_idx on public.finance_transactions(occurred_at);
create index if not exists finance_transactions_type_category_idx on public.finance_transactions(entry_type,category);
create unique index if not exists finance_transactions_source_unique_idx
  on public.finance_transactions(source_type,source_id)
  where source_type is not null and source_id is not null;

alter table public.finance_transactions enable row level security;
revoke all on public.finance_transactions from anon, authenticated;

drop function if exists public.admin_add_finance_transaction(timestamptz,text,text,numeric,text,uuid,text,uuid,text);
create function public.admin_add_finance_transaction(
  p_occurred_at timestamptz,
  p_entry_type text,
  p_category text,
  p_amount numeric,
  p_currency text default 'USD',
  p_partner_id uuid default null,
  p_source_type text default null,
  p_source_id uuid default null,
  p_notes text default null
) returns uuid
language plpgsql security definer set search_path=public
as $$
declare v_id uuid;
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  if p_entry_type not in ('revenue','expense') then raise exception 'INVALID_ENTRY_TYPE'; end if;
  if coalesce(p_amount,-1) <= 0 then raise exception 'INVALID_AMOUNT'; end if;
  if nullif(trim(p_category),'') is null then raise exception 'CATEGORY_REQUIRED'; end if;
  if lower(trim(p_category)) in ('gift','gifts','gift value','cashback','cashback balance','cashback liability','cashback_liability') then
    raise exception 'NON_OPERATING_CATEGORY';
  end if;
  if lower(trim(coalesce(p_source_type,'')))='partner_payment' then
    raise exception 'PARTNER_PAYMENTS_ARE_AUTOMATIC';
  end if;

  insert into public.finance_transactions(occurred_at,entry_type,category,amount,currency,partner_id,source_type,source_id,notes)
  values(coalesce(p_occurred_at,now()),p_entry_type,trim(p_category),p_amount,upper(coalesce(nullif(trim(p_currency),''),'USD')),p_partner_id,nullif(trim(coalesce(p_source_type,'')),''),p_source_id,p_notes)
  returning id into v_id;
  return v_id;
end $$;

drop function if exists public.admin_finance_pnl(timestamptz,timestamptz,text);
create function public.admin_finance_pnl(
  p_from timestamptz,
  p_to timestamptz,
  p_currency text default 'USD'
) returns table(
  gross_revenue numeric,
  operating_expenses numeric,
  taxes_reserve numeric,
  total_expenses numeric,
  net_profit numeric
)
language plpgsql stable security definer set search_path=public
as $$
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  return query
  with manual as (
    select f.entry_type,f.category,f.amount
    from public.finance_transactions f
    where f.occurred_at >= p_from and f.occurred_at < p_to
      and f.currency=upper(coalesce(nullif(trim(p_currency),''),'USD'))
  ), subscription_revenue as (
    select 'revenue'::text as entry_type,'Partner subscriptions'::text as category,pp.amount::numeric as amount
    from public.partner_payments pp
    where pp.status='confirmed'
      and pp.paid_at >= p_from and pp.paid_at < p_to
      and pp.currency=upper(coalesce(nullif(trim(p_currency),''),'USD'))
  ), all_entries as (
    select * from manual
    union all
    select * from subscription_revenue
  )
  select
    coalesce(sum(case when entry_type='revenue' then amount else 0 end),0)::numeric,
    coalesce(sum(case when entry_type='expense' and lower(category)<>'taxes / reserve' then amount else 0 end),0)::numeric,
    coalesce(sum(case when entry_type='expense' and lower(category)='taxes / reserve' then amount else 0 end),0)::numeric,
    coalesce(sum(case when entry_type='expense' then amount else 0 end),0)::numeric,
    (coalesce(sum(case when entry_type='revenue' then amount else 0 end),0)-coalesce(sum(case when entry_type='expense' then amount else 0 end),0))::numeric
  from all_entries;
end $$;

drop function if exists public.admin_finance_breakdown(timestamptz,timestamptz,text);
create function public.admin_finance_breakdown(
  p_from timestamptz,
  p_to timestamptz,
  p_currency text default 'USD'
) returns table(entry_type text,category text,amount numeric)
language plpgsql stable security definer set search_path=public
as $$
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  return query
  with all_entries as (
    select f.entry_type,f.category,f.amount
    from public.finance_transactions f
    where f.occurred_at >= p_from and f.occurred_at < p_to
      and f.currency=upper(coalesce(nullif(trim(p_currency),''),'USD'))
    union all
    select 'revenue'::text,'Partner subscriptions'::text,pp.amount::numeric
    from public.partner_payments pp
    where pp.status='confirmed'
      and pp.paid_at >= p_from and pp.paid_at < p_to
      and pp.currency=upper(coalesce(nullif(trim(p_currency),''),'USD'))
  )
  select a.entry_type,a.category,sum(a.amount)::numeric
  from all_entries a
  group by a.entry_type,a.category
  order by a.entry_type,a.category;
end $$;

-- Partner package tier (Bronze / Silver / Gold) is not currently stored on partners/subscriptions.
-- Until a reviewed tier field exists, confirmed subscription payments appear as "Partner subscriptions"
-- instead of guessing a package. This preserves accounting accuracy and avoids duplicated revenue.
-- Keep currencies separate; never silently add USD and LBP.

rollback;
