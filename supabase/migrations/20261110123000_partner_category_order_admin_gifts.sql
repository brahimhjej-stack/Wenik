begin;
create table public.partner_category_display_order (
  category text primary key check (char_length(category) between 1 and 60),
  partner_ids uuid[] not null
);
alter table public.partner_category_display_order enable row level security;
revoke all on public.partner_category_display_order from public, anon, authenticated;

create function public.public_partner_category_order()
returns jsonb language sql stable security definer set search_path = ''
as $$
  select coalesce(jsonb_object_agg(category, partner_ids), '{}'::jsonb)
  from public.partner_category_display_order;
$$;

create function public.admin_set_partner_category_order(p_category text, p_partner_ids uuid[])
returns void language plpgsql security definer set search_path = ''
as $$
begin
  if public.is_wenik_admin() is not true then
    raise exception 'ADMIN_REQUIRED' using errcode = '42501';
  end if;
  if p_partner_ids is null or cardinality(p_partner_ids) <>
    (select count(distinct partner_id) from unnest(p_partner_ids) as ids(partner_id)) then
    raise exception 'INVALID_PARTNER_ORDER';
  end if;
  insert into public.partner_category_display_order(category, partner_ids)
  values (lower(trim(p_category)), p_partner_ids)
  on conflict (category) do update set partner_ids = excluded.partner_ids;
end;
$$;

revoke all on function public.public_partner_category_order() from public;
grant execute on function public.public_partner_category_order() to anon, authenticated;
revoke all on function public.admin_set_partner_category_order(text, uuid[]) from public, anon;
grant execute on function public.admin_set_partner_category_order(text, uuid[]) to authenticated;

-- Close all overloads of the old partner write endpoints, including cached clients.
do $$
declare endpoint regprocedure;
begin
  for endpoint in
    select p.oid::regprocedure from pg_proc p
    join pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and p.proname in
      ('partner_submit_gift', 'partner_update_gift', 'partner_delete_gift')
  loop
    execute format('revoke execute on function %s from public, anon, authenticated', endpoint);
  end loop;
end;
$$;
revoke insert, update, delete, truncate on public.partner_gifts from public, anon, authenticated;
commit;
