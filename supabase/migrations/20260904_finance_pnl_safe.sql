-- WENIK Finance P&L — SAFE PREVIEW MIGRATION
-- Prepared on staging only. DO NOT apply to production until reviewed/tested.
-- Gifts and cashback liabilities are intentionally excluded from operating P&L.

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

alter table public.finance_transactions enable row level security;

-- No direct client table access. Finance goes through admin-only RPCs.
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
  if coalesce(p_amount,-1) < 0 then raise exception 'INVALID_AMOUNT'; end if;
  if nullif(trim(p_category),'') is null then raise exception 'CATEGORY_REQUIRED'; end if;
  if lower(trim(p_category)) in ('gift','gifts','cashback','cashback liability','cashback_liability') then
    raise exception 'NON_OPERATING_CATEGORY';
  end if;
  insert into public.finance_transactions(occurred_at,entry_type,category,amount,currency,partner_id,source_type,source_id,notes)
  values(coalesce(p_occurred_at,now()),p_entry_type,trim(p_category),p_amount,upper(coalesce(nullif(trim(p_currency),''),'USD')),p_partner_id,p_source_type,p_source_id,p_notes)
  returning id into v_id;
  return v_id;
end $$;

drop function if exists public.admin_finance_pnl(timestamptz,timestamptz,text);
create function public.admin_finance_pnl(
  p_from timestamptz,
  p_to timestamptz,
  p_currency text default 'USD'
) returns table(gross_revenue numeric,total_expenses numeric,net_profit numeric)
language plpgsql stable security definer set search_path=public
as $$
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  return query
  select
    coalesce(sum(case when f.entry_type='revenue' then f.amount else 0 end),0)::numeric,
    coalesce(sum(case when f.entry_type='expense' then f.amount else 0 end),0)::numeric,
    (coalesce(sum(case when f.entry_type='revenue' then f.amount else 0 end),0)-coalesce(sum(case when f.entry_type='expense' then f.amount else 0 end),0))::numeric
  from public.finance_transactions f
  where f.occurred_at >= p_from and f.occurred_at < p_to
    and f.currency=upper(coalesce(nullif(trim(p_currency),''),'USD'));
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
  select f.entry_type,f.category,sum(f.amount)::numeric
  from public.finance_transactions f
  where f.occurred_at >= p_from and f.occurred_at < p_to
    and f.currency=upper(coalesce(nullif(trim(p_currency),''),'USD'))
  group by f.entry_type,f.category
  order by f.entry_type,f.category;
end $$;

-- Existing confirmed partner subscription payments are revenue, but are not copied here.
-- A later reviewed migration/RPC can unify them into P&L without duplicating historical payments.
-- Keep currencies separate; never silently add USD and LBP.

rollback;
