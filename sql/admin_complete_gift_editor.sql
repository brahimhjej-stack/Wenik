create or replace function public.admin_gift_edit_inventory()
returns jsonb language plpgsql stable security definer set search_path=public as $$
begin
if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
return coalesce((select jsonb_agg(to_jsonb(g)||jsonb_build_object('gift_id',g.id,'gift_name',g.name,'partner_name',p.business_name,'images',coalesce((select jsonb_agg(i.image_url order by i.sort_order) from public.gift_images i where i.gift_id=g.id),'[]'::jsonb)) order by g.created_at desc) from public.partner_gifts g join public.partners p on p.id=g.partner_id),'[]'::jsonb);
end $$;
revoke all on function public.admin_gift_edit_inventory() from public,anon;
grant execute on function public.admin_gift_edit_inventory() to authenticated;
create or replace function public.admin_update_gift_details(p_gift_id uuid,p_expected_updated_at timestamptz,p_partner_id uuid,p_name text,p_description text,p_quantity integer,p_gift_value_usd numeric,p_regular_points integer,p_special_offer boolean,p_offer_points integer,p_images jsonb)
returns boolean language plpgsql security definer set search_path=public as $$
declare g public.partner_gifts%rowtype; v_effective integer; v_allocated integer; v_used integer; v_wenik boolean; v_image text;
begin
if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
select * into g from public.partner_gifts where id=p_gift_id for update;
if not found then raise exception 'GIFT_NOT_FOUND'; end if;
if g.updated_at is distinct from p_expected_updated_at then raise exception 'GIFT_CHANGED_RELOAD'; end if;
if nullif(trim(p_name),'') is null then raise exception 'GIFT_NAME_REQUIRED'; end if;
if p_quantity is null or p_quantity<1 then raise exception 'INVALID_QUANTITY'; end if;
if p_regular_points is null or p_regular_points<1 then raise exception 'INVALID_POINTS'; end if;
if p_gift_value_usd is not null and p_gift_value_usd<=0 then raise exception 'INVALID_GIFT_VALUE'; end if;
if p_special_offer is null or (p_special_offer and (p_offer_points is null or p_offer_points<1)) then raise exception 'INVALID_OFFER_POINTS'; end if;
if not exists(select 1 from public.partners where id=p_partner_id) then raise exception 'PARTNER_NOT_FOUND'; end if;
if p_images is null or jsonb_typeof(p_images)<>'array' then raise exception 'INVALID_IMAGES'; end if;
if jsonb_array_length(p_images)>5 or exists(select 1 from jsonb_array_elements(p_images) e where jsonb_typeof(e)<>'string' or (e #>> '{}') !~ '^https://') then raise exception 'INVALID_IMAGES'; end if;
perform 1 from public.prizes where partner_gift_id=g.id order by id for update;
select coalesce(sum(p.quantity),0) into v_allocated from public.prizes p join public.campaigns c on c.id=p.campaign_id where p.partner_gift_id=g.id and c.code<>'wenik-points-catalog';
select count(*) into v_used from public.points_redemptions r join public.prizes p on p.id=r.prize_id where p.partner_gift_id=g.id and r.status::text in ('pending','approved','collected');
if p_quantity<greatest(v_allocated,v_used) then raise exception 'QUANTITY_BELOW_RESERVED'; end if;
if p_partner_id<>g.partner_id and (v_used>0 or exists(select 1 from public.winners w join public.prizes p on p.id=w.prize_id where p.partner_gift_id=g.id and w.status::text<>'cancelled')) then raise exception 'PARTNER_HAS_EXISTING_RESERVATIONS'; end if;
v_effective:=case when p_special_offer then p_offer_points else p_regular_points end;
v_image:=p_images->>0;
select code='WENIK-GIFTS' into v_wenik from public.partners where id=p_partner_id;
update public.partner_gifts set partner_id=p_partner_id,name=trim(p_name),description=nullif(trim(p_description),''),quantity=p_quantity,gift_value_usd=p_gift_value_usd,regular_points_cost=p_regular_points,special_offer_active=p_special_offer,special_offer_points=case when p_special_offer then p_offer_points else null end,points_cost=v_effective,image_url=v_image,updated_at=now() where id=g.id;
delete from public.gift_images where gift_id=g.id;
insert into public.gift_images(gift_id,image_url,sort_order) select g.id,e.value,e.ordinality::smallint from jsonb_array_elements_text(p_images) with ordinality e(value,ordinality);
update public.prizes set partner_id=p_partner_id,title=trim(p_name),description=nullif(trim(p_description),''),stated_value=p_gift_value_usd,image_url=v_image,gift_provider=case when v_wenik then 'wenik' else 'partner' end where partner_gift_id=g.id;
update public.prizes p set quantity=p_quantity from public.campaigns c where p.campaign_id=c.id and c.code='wenik-points-catalog' and p.partner_gift_id=g.id;
update public.points_reward_catalog c set points_cost=v_effective,updated_at=now() from public.prizes p where c.prize_id=p.id and p.partner_gift_id=g.id;
return true;
end $$;
revoke all on function public.admin_update_gift_details(uuid,timestamptz,uuid,text,text,integer,numeric,integer,boolean,integer,jsonb) from public,anon;
grant execute on function public.admin_update_gift_details(uuid,timestamptz,uuid,text,text,integer,numeric,integer,boolean,integer,jsonb) to authenticated;