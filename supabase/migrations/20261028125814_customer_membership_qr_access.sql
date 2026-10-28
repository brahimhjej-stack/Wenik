-- Customer-paid access is independent of partner membership enforcement.
alter table public.whish_checkout_settings add column customer_membership_required boolean not null default false;

create function whish_private.customer_membership_available(p_customer uuid) returns boolean
language sql stable security definer set search_path='' as $$
 select not exists(select 1 from public.whish_checkout_settings where id=true and (customer_membership_required or enforce_member_access))
 or exists(select 1 from public.customers c join public.whish_customer_memberships m on m.customer_id=c.id where c.id=p_customer and c.status='active' and m.paid_until>now());
$$;
revoke all on function whish_private.customer_membership_available(uuid) from public,anon,authenticated;

create function public.whish_set_customer_membership_required(p_enabled boolean) returns void
language plpgsql security definer set search_path='' as $$
begin
 if auth.uid() is null or not public.is_wenik_super_admin() then raise exception 'NOT_AUTHORIZED'; end if;
 if p_enabled is null then raise exception 'INVALID_SETTINGS'; end if;
 update public.whish_checkout_settings set customer_membership_required=p_enabled,updated_at=now() where id=true;
 insert into public.audit_logs(actor_auth_user_id,actor_role,action,entity_type,entity_id,payload)
 values(auth.uid(),'super_admin','customer_membership_requirement_changed','whish_checkout_settings','true',jsonb_build_object('enabled',p_enabled));
end $$;
revoke all on function public.whish_set_customer_membership_required(boolean) from public,anon;
grant execute on function public.whish_set_customer_membership_required(boolean) to authenticated;

create or replace function whish_private.guard_transaction_membership() returns trigger
language plpgsql security definer set search_path='' as $$
begin
 if new.status<>'confirmed' then return new; end if;
 if tg_op='UPDATE' then
  if old.status='confirmed' and old.customer_id=new.customer_id and old.partner_id=new.partner_id then return new; end if;
 end if;
 if not whish_private.customer_membership_available(new.customer_id) then raise exception 'CUSTOMER_MEMBERSHIP_REQUIRED'; end if;
 if coalesce((select enforce_member_access from public.whish_checkout_settings where id=true),false)
 and not exists(select 1 from public.partners p join public.partner_subscriptions s on s.partner_id=p.id where p.id=new.partner_id and p.status='active' and s.status<>'suspended' and greatest(s.trial_ends_at,s.paid_until)>now()) then raise exception 'PARTNER_MEMBERSHIP_REQUIRED'; end if;
 return new;
end $$;
revoke all on function whish_private.guard_transaction_membership() from public,anon,authenticated;

create or replace function whish_private.guard_redemption_membership() returns trigger
language plpgsql security definer set search_path='' as $$
begin
 if not whish_private.customer_membership_available(new.customer_id) then raise exception 'CUSTOMER_MEMBERSHIP_REQUIRED'; end if;
 return new;
end $$;
revoke all on function whish_private.guard_redemption_membership() from public,anon,authenticated;

-- Preserve existing signatures, partner authorization and QR expiry checks.
do $$
declare d text; f regprocedure;
begin
 d:=pg_get_functiondef('public.customer_refresh_qr()'::regprocedure);
 if position('v_token:=gen_random_uuid()' in d)=0 then raise exception 'QR_REFRESH_DEFINITION_CHANGED'; end if;
 d:=replace(d,'v_token:=gen_random_uuid()','if not whish_private.customer_membership_available(v_customer) then raise exception ''CUSTOMER_MEMBERSHIP_REQUIRED''; end if; v_token:=gen_random_uuid()');
 execute d;
 d:=pg_get_functiondef('public.customer_my_profile()'::regprocedure);
 if position('c.qr_token,c.marketing_consent' in d)=0 then raise exception 'PROFILE_DEFINITION_CHANGED'; end if;
 d:=replace(d,'c.qr_token,c.marketing_consent','case when whish_private.customer_membership_available(c.id) then c.qr_token else null::uuid end,c.marketing_consent');
 execute d;
 foreach f in array array['public.partner_lookup_customer_by_qr(uuid)'::regprocedure,'public.partner_lookup_customer_by_qr_v2(uuid)'::regprocedure,'public.partner_lookup_customer_by_qr_v3(uuid)'::regprocedure] loop
  d:=pg_get_functiondef(f);
  if position('where c.qr_token' in d)=0 then raise exception 'QR_LOOKUP_DEFINITION_CHANGED'; end if;
  d:=replace(d,'where c.qr_token','where whish_private.customer_membership_available(c.id) and c.qr_expires_at>now() and c.qr_token');
  execute d;
 end loop;
end $$;
revoke all on function public.customer_refresh_qr(),public.customer_my_profile(),public.partner_lookup_customer_by_qr(uuid),public.partner_lookup_customer_by_qr_v2(uuid),public.partner_lookup_customer_by_qr_v3(uuid) from public,anon;
grant execute on function public.customer_refresh_qr(),public.customer_my_profile(),public.partner_lookup_customer_by_qr(uuid),public.partner_lookup_customer_by_qr_v2(uuid),public.partner_lookup_customer_by_qr_v3(uuid) to authenticated;
