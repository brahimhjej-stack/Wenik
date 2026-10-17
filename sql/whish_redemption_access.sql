-- Enforce only NEW requests. Expiry never cancels an already approved gift.
begin;
create function whish_private.guard_redemption_membership() returns trigger
language plpgsql security definer set search_path='' as $$
begin
 if not coalesce((select enforce_member_access from public.whish_checkout_settings where id=true),false) then return new; end if;
 if not exists(select 1 from public.customers c join public.whish_customer_memberships m on m.customer_id=c.id where c.id=new.customer_id and c.status='active' and m.paid_until>now()) then raise exception 'CUSTOMER_MEMBERSHIP_REQUIRED'; end if;
 return new;
end $$;
revoke all on function whish_private.guard_redemption_membership() from public,anon,authenticated;
create trigger whish_redemption_membership before insert on public.points_redemptions for each row execute function whish_private.guard_redemption_membership();
commit;
