-- WENIK flexible partner gift metadata (STAGING PREPARATION ONLY)
-- Gift benefits may be vouchers, discounts, experiences, items, services or other formats.
-- Historical rule: once a partner gift is assigned to a WIN campaign, its display metadata is snapshotted on the prize.
-- No production change: this preview is wrapped in a transaction and ROLLBACK.

begin;

alter table public.partner_gifts
  add column if not exists gift_type text,
  add column if not exists display_value text;

alter table public.partner_gifts drop constraint if exists partner_gifts_gift_type_check;
alter table public.partner_gifts add constraint partner_gifts_gift_type_check
  check (gift_type is null or gift_type in ('voucher','discount','experience','item','service','other'));

alter table public.prizes
  add column if not exists gift_type text,
  add column if not exists display_value text;

alter table public.prizes drop constraint if exists prizes_gift_type_check;
alter table public.prizes add constraint prizes_gift_type_check
  check (gift_type is null or gift_type in ('voucher','discount','experience','item','service','other'));

create or replace function public.partner_submit_gift_v2(
  p_name text,
  p_description text default null,
  p_quantity integer default 1,
  p_gift_type text default null,
  p_display_value text default null
)
returns uuid language plpgsql security definer set search_path=public as $$
declare v_partner uuid; v_id uuid; v_type text; v_display text;
begin
  v_partner:=public.current_partner_id();
  if v_partner is null then raise exception 'NOT_AUTHORIZED'; end if;
  if coalesce(trim(p_name),'')='' then raise exception 'GIFT_NAME_REQUIRED'; end if;
  if coalesce(p_quantity,0)<1 then raise exception 'INVALID_QUANTITY'; end if;
  v_type:=nullif(lower(trim(coalesce(p_gift_type,''))),'');
  v_display:=nullif(trim(coalesce(p_display_value,'')),'');
  if v_type is not null and v_type not in ('voucher','discount','experience','item','service','other') then raise exception 'INVALID_GIFT_TYPE'; end if;
  if length(coalesce(v_display,''))>120 then raise exception 'DISPLAY_VALUE_TOO_LONG'; end if;
  insert into public.partner_gifts(partner_id,name,description,quantity,approval_status,is_active,gift_type,display_value)
  values(v_partner,trim(p_name),nullif(trim(coalesce(p_description,'')),''),p_quantity,'pending',false,v_type,v_display)
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
returns boolean language plpgsql security definer set search_path=public as $$
declare v_partner uuid; v_used integer; v_type text; v_display text;
begin
  v_partner:=public.current_partner_id();
  if v_partner is null then raise exception 'NOT_AUTHORIZED'; end if;
  if coalesce(trim(p_name),'')='' then raise exception 'GIFT_NAME_REQUIRED'; end if;
  if coalesce(p_quantity,0)<1 then raise exception 'INVALID_QUANTITY'; end if;
  v_type:=nullif(lower(trim(coalesce(p_gift_type,''))),'');
  v_display:=nullif(trim(coalesce(p_display_value,'')),'');
  if v_type is not null and v_type not in ('voucher','discount','experience','item','service','other') then raise exception 'INVALID_GIFT_TYPE'; end if;
  if length(coalesce(v_display,''))>120 then raise exception 'DISPLAY_VALUE_TOO_LONG'; end if;
  select count(*) into v_used from public.winners w join public.prizes p on p.id=w.prize_id where p.partner_gift_id=p_gift_id and w.status<>'cancelled';
  if p_quantity<v_used then raise exception 'QUANTITY_BELOW_ALREADY_WON:%',v_used; end if;
  update public.partner_gifts set
    name=trim(p_name),description=nullif(trim(coalesce(p_description,'')),''),quantity=p_quantity,
    gift_type=v_type,display_value=v_display,approval_status='pending',is_active=false,
    reviewed_at=null,reviewed_by=null,review_note=null,updated_at=now()
  where id=p_gift_id and partner_id=v_partner;
  return found;
end $$;

-- New assignment RPC keeps the current inventory checks but snapshots the human-readable benefit.
-- The existing production RPC is intentionally not replaced by this preview.
create or replace function public.admin_assign_partner_gift_to_campaign_v2(
  p_campaign_id uuid,
  p_gift_id uuid,
  p_quantity integer default 1
)
returns uuid language plpgsql security definer set search_path=public as $$
declare v_gift public.partner_gifts%rowtype; v_reserved bigint; v_available bigint; v_prize uuid;
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  if coalesce(p_quantity,0)<1 then raise exception 'INVALID_QUANTITY'; end if;
  if not exists(select 1 from public.campaigns where id=p_campaign_id) then raise exception 'CAMPAIGN_NOT_FOUND'; end if;
  select * into v_gift from public.partner_gifts where id=p_gift_id for update;
  if not found then raise exception 'GIFT_NOT_FOUND'; end if;
  if v_gift.approval_status<>'approved' or not v_gift.is_active then raise exception 'GIFT_NOT_AVAILABLE'; end if;
  select coalesce(sum(p.quantity),0) into v_reserved from public.prizes p where p.partner_gift_id=p_gift_id;
  v_available:=greatest(v_gift.quantity::bigint-v_reserved,0);
  if p_quantity>v_available then raise exception 'INSUFFICIENT_GIFT_INVENTORY:%',v_available; end if;
  insert into public.prizes(campaign_id,partner_id,title,description,quantity,partner_gift_id,gift_type,display_value)
  values(p_campaign_id,v_gift.partner_id,v_gift.name,v_gift.description,p_quantity,v_gift.id,v_gift.gift_type,v_gift.display_value)
  returning id into v_prize;
  return v_prize;
end $$;

-- Customer feed reads the prize snapshot, never mutable partner_gifts metadata.
create or replace function public.public_active_win_gifts(p_limit integer default 100)
returns table(
  prize_id uuid,campaign_id uuid,campaign_title text,campaign_status text,partner_id uuid,
  partner_name text,partner_logo_url text,partner_gift_id uuid,gift_title text,gift_description text,
  gift_type text,display_value text,stated_value numeric,conditions text,expires_at timestamptz,
  original_quantity integer,won_quantity bigint,remaining_quantity bigint
)
language sql stable security definer set search_path=public as $$
  select p.id,p.campaign_id,c.title,c.status::text,p.partner_id,
    coalesce(pt.business_name,'WENIK Partner'),pt.logo_url,p.partner_gift_id,p.title,p.description,
    p.gift_type,p.display_value,p.stated_value,p.conditions,p.expires_at,p.quantity,
    count(w.id) filter(where w.status::text<>'cancelled'),
    greatest(p.quantity::bigint-count(w.id) filter(where w.status::text<>'cancelled'),0)
  from public.prizes p
  join public.campaigns c on c.id=p.campaign_id
  left join public.partners pt on pt.id=p.partner_id
  left join public.winners w on w.prize_id=p.id
  where c.status::text='active'
    and (c.starts_at is null or c.starts_at<=now())
    and (c.ends_at is null or c.ends_at>=now())
    and (p.expires_at is null or p.expires_at>=now())
  group by p.id,p.campaign_id,c.title,c.status,p.partner_id,pt.business_name,pt.logo_url,p.partner_gift_id,p.title,p.description,p.gift_type,p.display_value,p.stated_value,p.conditions,p.expires_at,p.quantity,p.created_at,c.starts_at
  having greatest(p.quantity::bigint-count(w.id) filter(where w.status::text<>'cancelled'),0)>0
  order by c.starts_at nulls first,p.created_at,p.id
  limit greatest(1,least(coalesce(p_limit,100),200));
$$;

revoke all on function public.partner_submit_gift_v2(text,text,integer,text,text) from public;
grant execute on function public.partner_submit_gift_v2(text,text,integer,text,text) to authenticated;
revoke all on function public.partner_update_gift_v2(uuid,text,text,integer,text,text) from public;
grant execute on function public.partner_update_gift_v2(uuid,text,text,integer,text,text) to authenticated;
revoke all on function public.admin_assign_partner_gift_to_campaign_v2(uuid,uuid,integer) from public;
grant execute on function public.admin_assign_partner_gift_to_campaign_v2(uuid,uuid,integer) to authenticated;
revoke all on function public.public_active_win_gifts(integer) from public;
grant execute on function public.public_active_win_gifts(integer) to anon,authenticated;

rollback;
-- Intentionally ROLLBACK: contract preview only. Production Supabase remains untouched.
