-- WENIK flexible partner gift metadata (STAGING PREPARATION ONLY)
-- Supports vouchers, discounts, experiences, items, services and other gift formats.
-- No production change: this preview is wrapped in a transaction and ROLLBACK.

begin;

alter table public.partner_gifts
  add column if not exists gift_type text,
  add column if not exists display_value text;

alter table public.partner_gifts
  drop constraint if exists partner_gifts_gift_type_check;

alter table public.partner_gifts
  add constraint partner_gifts_gift_type_check
  check (gift_type is null or gift_type in ('voucher','discount','experience','item','service','other'));

create or replace function public.partner_submit_gift_v2(
  p_name text,
  p_description text default null,
  p_quantity integer default 1,
  p_gift_type text default null,
  p_display_value text default null
)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare v_partner uuid; v_id uuid; v_type text;
begin
  v_partner:=public.current_partner_id();
  if v_partner is null then raise exception 'NOT_AUTHORIZED'; end if;
  if coalesce(trim(p_name),'')='' then raise exception 'GIFT_NAME_REQUIRED'; end if;
  if coalesce(p_quantity,0)<1 then raise exception 'INVALID_QUANTITY'; end if;
  v_type:=nullif(lower(trim(coalesce(p_gift_type,''))), '');
  if v_type is not null and v_type not in ('voucher','discount','experience','item','service','other') then
    raise exception 'INVALID_GIFT_TYPE';
  end if;
  insert into public.partner_gifts(partner_id,name,description,quantity,approval_status,is_active,gift_type,display_value)
  values(v_partner,trim(p_name),nullif(trim(coalesce(p_description,'')),''),p_quantity,'pending',false,v_type,nullif(trim(coalesce(p_display_value,'')),''))
  returning id into v_id;
  return v_id;
end $$;

create or replace function public.partner_update_gift_v2(
  p_gift_id uuid,
  p_name text,
  p_description text default null,
  p_quantity integer default 1,
  p_gift_type text default null,
  p_display_value text default null
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare v_partner uuid; v_used integer; v_type text;
begin
  v_partner:=public.current_partner_id();
  if v_partner is null then raise exception 'NOT_AUTHORIZED'; end if;
  if coalesce(trim(p_name),'')='' then raise exception 'GIFT_NAME_REQUIRED'; end if;
  if coalesce(p_quantity,0)<1 then raise exception 'INVALID_QUANTITY'; end if;
  v_type:=nullif(lower(trim(coalesce(p_gift_type,''))), '');
  if v_type is not null and v_type not in ('voucher','discount','experience','item','service','other') then
    raise exception 'INVALID_GIFT_TYPE';
  end if;
  select count(*) into v_used
  from public.winners w
  join public.prizes p on p.id=w.prize_id
  where p.partner_gift_id=p_gift_id and w.status<>'cancelled';
  if p_quantity < v_used then raise exception 'QUANTITY_BELOW_ALREADY_WON:%',v_used; end if;
  update public.partner_gifts
  set name=trim(p_name),
      description=nullif(trim(coalesce(p_description,'')),''),
      quantity=p_quantity,
      gift_type=v_type,
      display_value=nullif(trim(coalesce(p_display_value,'')),''),
      approval_status='pending',
      is_active=false,
      reviewed_at=null,
      reviewed_by=null,
      review_note=null,
      updated_at=now()
  where id=p_gift_id and partner_id=v_partner;
  return found;
end $$;

-- Replaces the public feed only inside this preview transaction so the customer UI
-- can consume a human-readable type/value without assuming a currency.
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
  gift_type text,
  display_value text,
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
    p.id,p.campaign_id,c.title,c.status::text,p.partner_id,
    coalesce(pt.business_name,'WENIK Partner'),pt.logo_url,p.partner_gift_id,
    p.title,p.description,pg.gift_type,pg.display_value,p.stated_value,p.conditions,p.expires_at,p.quantity,
    count(w.id) filter (where w.status::text <> 'cancelled') as won_quantity,
    greatest(p.quantity::bigint-count(w.id) filter (where w.status::text <> 'cancelled'),0) as remaining_quantity
  from public.prizes p
  join public.campaigns c on c.id=p.campaign_id
  left join public.partners pt on pt.id=p.partner_id
  left join public.partner_gifts pg on pg.id=p.partner_gift_id
  left join public.winners w on w.prize_id=p.id
  where c.status::text='active'
    and (c.starts_at is null or c.starts_at<=now())
    and (c.ends_at is null or c.ends_at>=now())
    and (p.expires_at is null or p.expires_at>=now())
  group by p.id,p.campaign_id,c.title,c.status,p.partner_id,pt.business_name,pt.logo_url,p.partner_gift_id,p.title,p.description,pg.gift_type,pg.display_value,p.stated_value,p.conditions,p.expires_at,p.quantity,p.created_at,c.starts_at
  having greatest(p.quantity::bigint-count(w.id) filter (where w.status::text <> 'cancelled'),0)>0
  order by c.starts_at nulls first,p.created_at,p.id
  limit greatest(1,least(coalesce(p_limit,100),200));
$$;

revoke all on function public.partner_submit_gift_v2(text,text,integer,text,text) from public;
grant execute on function public.partner_submit_gift_v2(text,text,integer,text,text) to authenticated;
revoke all on function public.partner_update_gift_v2(uuid,text,text,integer,text,text) from public;
grant execute on function public.partner_update_gift_v2(uuid,text,text,integer,text,text) to authenticated;
revoke all on function public.public_active_win_gifts(integer) from public;
grant execute on function public.public_active_win_gifts(integer) to anon,authenticated;

rollback;
-- Intentionally ROLLBACK: preview contract only. Apply to a Supabase development branch before production.
