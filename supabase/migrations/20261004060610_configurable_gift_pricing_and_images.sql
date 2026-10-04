-- WENIK gift pricing: the default is USD value x 150 points.
-- The multiplier is global and editable by a super admin. Individual gifts can
-- use an explicit points override for sponsored/free special offers.

alter table public.points_settings
  add column if not exists gift_points_per_usd numeric(12,2) not null default 150;

alter table public.points_settings
  drop constraint if exists points_settings_gift_points_per_usd_check;
alter table public.points_settings
  add constraint points_settings_gift_points_per_usd_check
  check (gift_points_per_usd > 0);

alter table public.partner_gifts
  add column if not exists gift_value_usd numeric(12,2),
  add column if not exists regular_points_cost integer,
  add column if not exists special_offer_points integer,
  add column if not exists special_offer_active boolean not null default false;

alter table public.partner_gifts
  drop constraint if exists partner_gifts_gift_value_usd_check;
alter table public.partner_gifts
  add constraint partner_gifts_gift_value_usd_check
  check (gift_value_usd is null or gift_value_usd >= 0);

alter table public.partner_gifts
  drop constraint if exists partner_gifts_regular_points_cost_check;
alter table public.partner_gifts
  add constraint partner_gifts_regular_points_cost_check
  check (regular_points_cost is null or regular_points_cost > 0);

alter table public.partner_gifts
  drop constraint if exists partner_gifts_special_offer_points_check;
alter table public.partner_gifts
  add constraint partner_gifts_special_offer_points_check
  check (special_offer_points is null or special_offer_points > 0);

update public.partner_gifts
set regular_points_cost = coalesce(regular_points_cost, points_cost)
where points_cost is not null;

create table if not exists public.gift_images (
  id uuid primary key default gen_random_uuid(),
  gift_id uuid not null references public.partner_gifts(id) on delete cascade,
  image_url text not null,
  sort_order smallint not null default 1 check (sort_order between 1 and 5),
  created_at timestamptz not null default now(),
  unique (gift_id, sort_order)
);

alter table public.gift_images enable row level security;
revoke all on table public.gift_images from anon, authenticated;

insert into public.gift_images(gift_id, image_url, sort_order)
select id, image_url, 1
from public.partner_gifts
where nullif(trim(image_url), '') is not null
on conflict (gift_id, sort_order) do nothing;

create or replace function public.admin_gift_pricing_settings()
returns table(gift_points_per_usd numeric)
language sql
stable
security definer
set search_path = public
as $$
  select s.gift_points_per_usd
  from public.points_settings s
  where s.id = true
    and public.is_wenik_admin();
$$;

create or replace function public.admin_set_gift_pricing_multiplier(p_gift_points_per_usd numeric)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
begin
  if not exists (
    select 1 from public.admin_users
    where auth_user_id = auth.uid()
      and is_active = true
      and role = 'super_admin'
  ) then
    raise exception 'SUPER_ADMIN_REQUIRED';
  end if;
  if coalesce(p_gift_points_per_usd, 0) <= 0 then
    raise exception 'INVALID_GIFT_MULTIPLIER';
  end if;
  update public.points_settings
  set gift_points_per_usd = p_gift_points_per_usd,
      updated_at = now(),
      updated_by = auth.uid()
  where id = true;
  return found;
end;
$$;

create or replace function public.admin_create_priced_partner_gift(
  p_partner_id uuid,
  p_name text,
  p_description text default null,
  p_quantity integer default 1,
  p_gift_value_usd numeric default null,
  p_points_override integer default null,
  p_special_offer boolean default false
)
returns uuid
language plpgsql
security definer
set search_path = public
as $$
declare
  v_id uuid;
  v_admin uuid;
  v_campaign uuid;
  v_prize uuid;
  v_is_wenik boolean;
  v_multiplier numeric;
  v_regular integer;
  v_effective integer;
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  if p_partner_id is null or not exists(select 1 from public.partners where id=p_partner_id) then raise exception 'PARTNER_NOT_FOUND'; end if;
  if nullif(trim(coalesce(p_name,'')),'') is null then raise exception 'GIFT_NAME_REQUIRED'; end if;
  if coalesce(p_quantity,0)<1 then raise exception 'INVALID_QUANTITY'; end if;
  if coalesce(p_gift_value_usd,0)<=0 then raise exception 'GIFT_VALUE_REQUIRED'; end if;
  if p_points_override is not null and p_points_override<1 then raise exception 'INVALID_POINTS_OVERRIDE'; end if;

  select gift_points_per_usd into v_multiplier from public.points_settings where id=true;
  v_multiplier := coalesce(v_multiplier,150);
  v_regular := ceil(p_gift_value_usd*v_multiplier)::integer;
  v_effective := case when coalesce(p_special_offer,false) and p_points_override is not null
                      then p_points_override else v_regular end;

  select id into v_admin from public.admin_users where auth_user_id=auth.uid() and is_active=true limit 1;
  select exists(select 1 from public.partners where id=p_partner_id and code='WENIK-GIFTS') into v_is_wenik;

  insert into public.partner_gifts(
    partner_id,name,description,quantity,points_cost,gift_value_usd,
    regular_points_cost,special_offer_points,special_offer_active,
    approval_status,is_active,reviewed_at,reviewed_by,updated_at
  ) values (
    p_partner_id,trim(p_name),nullif(trim(coalesce(p_description,'')),''),p_quantity,
    v_effective,p_gift_value_usd,v_regular,
    case when coalesce(p_special_offer,false) then p_points_override else null end,
    coalesce(p_special_offer,false) and p_points_override is not null,
    'approved',true,now(),v_admin,now()
  ) returning id into v_id;

  select id into v_campaign from public.campaigns where code='wenik-points-catalog' limit 1;
  if v_campaign is null then
    insert into public.campaigns(code,title,description,status,terms)
    values('wenik-points-catalog','WENIK Points Catalog','Internal catalog used for Points redemption','draft','Not a WIN draw campaign')
    returning id into v_campaign;
  end if;

  insert into public.prizes(
    campaign_id,partner_id,partner_gift_id,title,description,quantity,
    stated_value,gift_provider,fulfillment_instructions
  ) values (
    v_campaign,p_partner_id,v_id,trim(p_name),nullif(trim(coalesce(p_description,'')),''),p_quantity,
    p_gift_value_usd,case when v_is_wenik then 'wenik' else 'partner' end,
    case when v_is_wenik then 'Contact WENIK to arrange receiving your gift.' else null end
  ) returning id into v_prize;

  insert into public.points_reward_catalog(prize_id,points_cost,is_active)
  values(v_prize,v_effective,true);
  return v_id;
end;
$$;

create or replace function public.admin_update_gift_pricing(
  p_gift_id uuid,
  p_gift_value_usd numeric,
  p_points_override integer default null,
  p_special_offer boolean default false
)
returns table(regular_points integer, effective_points integer)
language plpgsql
security definer
set search_path = public
as $$
declare
  v_multiplier numeric;
  v_regular integer;
  v_effective integer;
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  if coalesce(p_gift_value_usd,0)<=0 then raise exception 'GIFT_VALUE_REQUIRED'; end if;
  if p_points_override is not null and p_points_override<1 then raise exception 'INVALID_POINTS_OVERRIDE'; end if;
  select gift_points_per_usd into v_multiplier from public.points_settings where id=true;
  v_regular := ceil(p_gift_value_usd*coalesce(v_multiplier,150))::integer;
  v_effective := case when coalesce(p_special_offer,false) and p_points_override is not null
                      then p_points_override else v_regular end;

  update public.partner_gifts
  set gift_value_usd=p_gift_value_usd,
      regular_points_cost=v_regular,
      special_offer_points=case when coalesce(p_special_offer,false) then p_points_override else null end,
      special_offer_active=coalesce(p_special_offer,false) and p_points_override is not null,
      points_cost=v_effective,
      updated_at=now()
  where id=p_gift_id;
  if not found then raise exception 'GIFT_NOT_FOUND'; end if;

  update public.prizes set stated_value=p_gift_value_usd where partner_gift_id=p_gift_id;
  update public.points_reward_catalog c
  set points_cost=v_effective,updated_at=now()
  from public.prizes p
  where c.prize_id=p.id and p.partner_gift_id=p_gift_id;

  return query select v_regular,v_effective;
end;
$$;

create or replace function public.admin_gift_pricing_inventory()
returns table(
  gift_id uuid, partner_name text, gift_name text, quantity integer,
  gift_value_usd numeric, regular_points_cost integer,
  special_offer_points integer, special_offer_active boolean,
  effective_points_cost integer
)
language sql
stable
security definer
set search_path = public
as $$
  select g.id,p.business_name,g.name,g.quantity,g.gift_value_usd,
         coalesce(g.regular_points_cost,g.points_cost),g.special_offer_points,
         g.special_offer_active,g.points_cost
  from public.partner_gifts g
  join public.partners p on p.id=g.partner_id
  where public.is_wenik_admin()
  order by g.created_at desc;
$$;

create or replace function public.admin_add_partner_gift_image(
  p_gift_id uuid,
  p_image_url text,
  p_sort_order integer default 1
)
returns boolean
language plpgsql
security definer
set search_path = public
as $$
declare v_url text := nullif(trim(coalesce(p_image_url,'')),'');
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  if v_url is null then raise exception 'IMAGE_URL_REQUIRED'; end if;
  if coalesce(p_sort_order,0) not between 1 and 5 then raise exception 'INVALID_IMAGE_ORDER'; end if;
  if not exists(select 1 from public.partner_gifts where id=p_gift_id) then raise exception 'GIFT_NOT_FOUND'; end if;
  insert into public.gift_images(gift_id,image_url,sort_order)
  values(p_gift_id,v_url,p_sort_order)
  on conflict(gift_id,sort_order) do update set image_url=excluded.image_url,created_at=now();
  if p_sort_order=1 then
    update public.partner_gifts set image_url=v_url,updated_at=now() where id=p_gift_id;
    update public.prizes set image_url=v_url where partner_gift_id=p_gift_id;
  end if;
  return true;
end;
$$;

create or replace function public.customer_points_reward_catalog_v2()
returns table(
  catalog_id uuid, prize_id uuid, gift_title text, gift_description text,
  partner_id uuid, partner_name text, partner_logo_url text,
  points_cost integer, regular_points_cost integer, special_offer_active boolean,
  gift_value_usd numeric, remaining_quantity bigint, gift_provider text,
  fulfillment_instructions text, fulfillment_phone text,
  gift_image_url text, gift_image_urls text[]
)
language sql
stable
security definer
set search_path = public
as $$
  with winner_use as (
    select prize_id,count(*)::bigint used from public.winners
    where status::text<>'cancelled' group by prize_id
  ), redemption_use as (
    select prize_id,count(*)::bigint used from public.points_redemptions
    where status in ('pending','approved','collected') group by prize_id
  )
  select rc.id,p.id,p.title,p.description,p.partner_id,
         case when p.gift_provider='wenik' then 'WENIK' else coalesce(pt.business_name,'WENIK Partner') end,
         pt.logo_url,rc.points_cost,coalesce(pg.regular_points_cost,rc.points_cost),
         coalesce(pg.special_offer_active,false),coalesce(pg.gift_value_usd,p.stated_value),
         greatest(p.quantity::bigint-coalesce(wu.used,0)-coalesce(ru.used,0),0),
         p.gift_provider,p.fulfillment_instructions,p.fulfillment_phone,
         coalesce(p.image_url,pg.image_url),
         coalesce(
           (select array_agg(gi.image_url order by gi.sort_order) from public.gift_images gi where gi.gift_id=pg.id),
           case when coalesce(p.image_url,pg.image_url) is not null then array[coalesce(p.image_url,pg.image_url)] else array[]::text[] end
         )
  from public.points_reward_catalog rc
  join public.prizes p on p.id=rc.prize_id
  left join public.partners pt on pt.id=p.partner_id
  left join public.partner_gifts pg on pg.id=p.partner_gift_id
  left join winner_use wu on wu.prize_id=p.id
  left join redemption_use ru on ru.prize_id=p.id
  where rc.is_active=true
    and (p.expires_at is null or p.expires_at>=now())
    and greatest(p.quantity::bigint-coalesce(wu.used,0)-coalesce(ru.used,0),0)>0
    and auth.uid() is not null
  order by rc.points_cost,p.created_at;
$$;

revoke all on function public.admin_gift_pricing_settings() from public, anon;
revoke all on function public.admin_set_gift_pricing_multiplier(numeric) from public, anon;
revoke all on function public.admin_create_priced_partner_gift(uuid,text,text,integer,numeric,integer,boolean) from public, anon;
revoke all on function public.admin_update_gift_pricing(uuid,numeric,integer,boolean) from public, anon;
revoke all on function public.admin_gift_pricing_inventory() from public, anon;
revoke all on function public.admin_add_partner_gift_image(uuid,text,integer) from public, anon;
revoke all on function public.customer_points_reward_catalog_v2() from public, anon;

grant execute on function public.admin_gift_pricing_settings() to authenticated;
grant execute on function public.admin_set_gift_pricing_multiplier(numeric) to authenticated;
grant execute on function public.admin_create_priced_partner_gift(uuid,text,text,integer,numeric,integer,boolean) to authenticated;
grant execute on function public.admin_update_gift_pricing(uuid,numeric,integer,boolean) to authenticated;
grant execute on function public.admin_gift_pricing_inventory() to authenticated;
grant execute on function public.admin_add_partner_gift_image(uuid,text,integer) to authenticated;
grant execute on function public.customer_points_reward_catalog_v2() to authenticated;
