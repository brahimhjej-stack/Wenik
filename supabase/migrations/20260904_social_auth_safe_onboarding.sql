-- WENIK social-auth onboarding (STAGING PREPARATION ONLY)
-- Do not apply to production until tested against a Supabase development branch.
-- Goal: allow Google/Facebook OAuth identities without weakening WENIK's mandatory
-- verified-mobile requirement for customer activation.

begin;

-- 1) Keep the existing phone/password signup path unchanged.
-- 2) OAuth users may exist in auth.users before a public.customers row exists.
-- 3) A customer row is created only after names + terms/privacy + verified phone exist.

create or replace function public.customer_complete_social_signup(
  p_first_name text,
  p_last_name text,
  p_marketing_consent boolean default false
)
returns table(customer_id uuid, wenik_id text, mobile text)
language plpgsql
security definer
set search_path = public, auth
as $$
declare
  v_uid uuid := auth.uid();
  v_user auth.users%rowtype;
  v_customer public.customers%rowtype;
begin
  if v_uid is null then raise exception 'AUTH_REQUIRED'; end if;

  select * into v_user from auth.users where id = v_uid;
  if not found then raise exception 'AUTH_REQUIRED'; end if;

  if nullif(trim(coalesce(p_first_name,'')),'') is null
     or nullif(trim(coalesce(p_last_name,'')),'') is null then
    raise exception 'NAME_REQUIRED';
  end if;

  -- WENIK rule: a customer account is not activated without a verified mobile.
  if v_user.phone is null or v_user.phone_confirmed_at is null then
    raise exception 'VERIFIED_PHONE_REQUIRED';
  end if;

  insert into public.customers(
    auth_user_id, wenik_id, first_name, last_name, mobile, mobile_verified,
    marketing_consent, marketing_consent_at,
    terms_accepted_at, privacy_accepted_at, status, joined_at
  )
  values(
    v_uid, public.generate_wenik_id(), trim(p_first_name), trim(p_last_name),
    v_user.phone, true,
    coalesce(p_marketing_consent,false),
    case when coalesce(p_marketing_consent,false) then now() end,
    now(), now(), 'active', now()
  )
  on conflict(auth_user_id) do update set
    first_name = excluded.first_name,
    last_name = excluded.last_name,
    mobile = excluded.mobile,
    mobile_verified = true,
    marketing_consent = excluded.marketing_consent,
    marketing_consent_at = case
      when excluded.marketing_consent then coalesce(public.customers.marketing_consent_at, now())
      else public.customers.marketing_consent_at
    end,
    terms_accepted_at = coalesce(public.customers.terms_accepted_at, now()),
    privacy_accepted_at = coalesce(public.customers.privacy_accepted_at, now()),
    status = 'active',
    updated_at = now()
  returning * into v_customer;

  return query select v_customer.id, v_customer.wenik_id, v_customer.mobile;
end;
$$;

revoke all on function public.customer_complete_social_signup(text,text,boolean) from public;
grant execute on function public.customer_complete_social_signup(text,text,boolean) to authenticated;

-- NOTE: handle_new_auth_user() must be adjusted in the development branch so that
-- OAuth identities are allowed to exist without immediately creating customers,
-- while the current phone/password signup behavior remains unchanged.
-- That trigger change is intentionally not included here until tested against the
-- exact auth provider metadata returned by Google and Facebook.

rollback;
-- Intentionally ROLLBACK in source preparation. Replace with COMMIT only after
-- development-branch testing and review.
