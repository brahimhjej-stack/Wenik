create function public.admin_partner_editor_list()
returns jsonb language plpgsql stable security definer set search_path = '' as $$
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  return coalesce((select jsonb_agg(jsonb_build_object(
    'id',p.id,'business_name',p.business_name,'category',p.category,'address',p.address,
    'phone',p.phone,'logo_url',p.logo_url,'social_links',p.social_links,'updated_at',p.updated_at,
    'discount',case when b.id is not null then to_jsonb(b) end
  ) order by p.business_name)
  from public.partners p left join lateral (
    select pb.* from public.partner_benefits pb where pb.partner_id=p.id and pb.is_active
      and (pb.starts_at is null or pb.starts_at<=now()) and (pb.ends_at is null or pb.ends_at>=now())
    order by pb.created_at desc limit 1
  ) b on true where p.code not in ('WENIK-GIFTS','WENIK-E2E-TEST')), '[]'::jsonb);
end $$;

create function public.admin_save_partner_editor(p_id uuid,p_updated_at timestamptz,p_name text,p_category text,
  p_address text,p_phone text,p_logo text,p_links jsonb,p_change_discount boolean,p_discount_id uuid,p_percent numeric,p_conditions text)
returns void language plpgsql security definer set search_path = '' as $$
declare v_b public.partner_benefits%rowtype;
begin
  if not public.is_wenik_admin() then raise exception 'NOT_AUTHORIZED'; end if;
  if nullif(btrim(p_name),'') is null or nullif(btrim(p_category),'') is null then
    raise exception 'Business name and category are required';
  end if;
  if p_change_discount and (p_percent is null or not (p_percent > 0 and p_percent <= 100)) then
    raise exception 'Enter a discount greater than 0 and at most 100';
  end if;
  update public.partners set business_name=btrim(p_name),category=btrim(p_category),
    address=nullif(btrim(p_address),''),phone=nullif(btrim(p_phone),''),logo_url=nullif(btrim(p_logo),''),
    social_links=jsonb_strip_nulls(social_links || coalesce(p_links,'{}'::jsonb)),updated_at=clock_timestamp()
  where id=p_id and updated_at=p_updated_at and code not in ('WENIK-GIFTS','WENIK-E2E-TEST');
  if not found then raise exception 'Partner changed. Refresh and try again.'; end if;
  if p_change_discount then
    select * into v_b from public.partner_benefits b where b.partner_id=p_id and b.is_active
      and (b.starts_at is null or b.starts_at<=now()) and (b.ends_at is null or b.ends_at>=now())
    order by b.created_at desc limit 1 for update;
    if v_b.id is distinct from p_discount_id then raise exception 'Discount changed. Refresh and try again.'; end if;
    if v_b.id is null then
      insert into public.partner_benefits(partner_id,title,benefit_type,benefit_value,conditions)
      values(p_id,p_percent::text || '% OFF','discount_percent',p_percent,nullif(btrim(p_conditions),''));
    elsif v_b.benefit_type='discount_percent' then
      update public.partner_benefits set benefit_value=p_percent,conditions=nullif(btrim(p_conditions),''),
        title=case when benefit_value is distinct from p_percent then p_percent::text || '% OFF' else title end
      where id=v_b.id;
    else raise exception 'This partner already has a different type of offer';
    end if;
  end if;
  insert into public.audit_logs(actor_auth_user_id,actor_role,action,entity_type,entity_id,payload)
  values(auth.uid(),(select role::text from public.admin_users where auth_user_id=auth.uid() and is_active limit 1),
    'admin_partner_updated','partner',p_id::text,jsonb_build_object('discount_changed',p_change_discount,'percent',p_percent));
end $$;
revoke all on function public.admin_partner_editor_list() from public,anon;
revoke all on function public.admin_save_partner_editor(uuid,timestamptz,text,text,text,text,text,jsonb,boolean,uuid,numeric,text) from public,anon;
grant execute on function public.admin_partner_editor_list() to authenticated;
grant execute on function public.admin_save_partner_editor(uuid,timestamptz,text,text,text,text,text,jsonb,boolean,uuid,numeric,text) to authenticated;
