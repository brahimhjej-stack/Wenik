-- WENIK WIN gift feed (STAGING PREPARATION ONLY)
-- Contract-audited read-only customer/public feed.
-- Never deletes or mutates gift/winner history.
-- Remaining inventory is derived from prize quantity minus non-cancelled winners.
-- Verified campaign_status values: draft, active, closed, drawn, archived.
-- Verified winner_status includes cancelled.
-- Do not apply to production until reviewed/tested in a Supabase development environment.

begin;

create or replace function public.public_active_win_gifts(p_limit integer default 100)
returns table(
  prize_id uuid,
  campaign_id uuid,
  campaign_title text,
  campaign_status text,
  partner_id uuid,
  partner_name text,
  partner_logo_url text,
  partner_gift_id uuid,
  gift_title text,
  gift_description text,
  stated_value numeric,
  conditions text,
  expires_at timestamptz,
  original_quantity integer,
  won_quantity bigint,
  remaining_quantity bigint
)
language sql
stable
security definer
set search_path = public
as $$
  select
    p.id,
    p.campaign_id,
    c.title,
    c.status::text,
    p.partner_id,
    coalesce(pt.business_name, 'WENIK Partner'),
    pt.logo_url,
    p.partner_gift_id,
    p.title,
    p.description,
    p.stated_value,
    p.conditions,
    p.expires_at,
    p.quantity,
    count(w.id) filter (where w.status::text <> 'cancelled') as won_quantity,
    greatest(p.quantity::bigint - count(w.id) filter (where w.status::text <> 'cancelled'), 0) as remaining_quantity
  from public.prizes p
  join public.campaigns c on c.id = p.campaign_id
  left join public.partners pt on pt.id = p.partner_id
  left join public.winners w on w.prize_id = p.id
  where c.status::text = 'active'
    and (c.starts_at is null or c.starts_at <= now())
    and (c.ends_at is null or c.ends_at >= now())
    and (p.expires_at is null or p.expires_at >= now())
  group by p.id,p.campaign_id,c.title,c.status,p.partner_id,pt.business_name,pt.logo_url,p.partner_gift_id,p.title,p.description,p.stated_value,p.conditions,p.expires_at,p.quantity,p.created_at,c.starts_at
  having greatest(p.quantity::bigint - count(w.id) filter (where w.status::text <> 'cancelled'), 0) > 0
  order by c.starts_at nulls first, p.created_at, p.id
  limit greatest(1, least(coalesce(p_limit,100),200));
$$;

revoke all on function public.public_active_win_gifts(integer) from public;
grant execute on function public.public_active_win_gifts(integer) to anon, authenticated;

rollback;
-- Intentionally ROLLBACK: source preview only. Replace with COMMIT only after safe DB testing/review.
