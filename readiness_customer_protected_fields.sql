create or replace function public.wenik_guard_customer_fields()
returns trigger language plpgsql set search_path=public as $$
begin
 if current_user in ('anon','authenticated') and not public.is_wenik_admin() then
  if (to_jsonb(new) - array['first_name','last_name','marketing_consent','marketing_consent_at','updated_at'])
     is distinct from
     (to_jsonb(old) - array['first_name','last_name','marketing_consent','marketing_consent_at','updated_at']) then
   raise exception 'CUSTOMER_PROTECTED_FIELDS' using errcode='42501';
  end if;
 end if;
 return new;
end $$;
revoke all on function public.wenik_guard_customer_fields() from public,anon,authenticated;
create trigger wenik_guard_customer_fields before update on public.customers
for each row execute function public.wenik_guard_customer_fields();