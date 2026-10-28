-- Apply after whish_checkout.sql; this only exposes the caller's membership.
begin;
create or replace function public.customer_my_billing_status()
returns jsonb language plpgsql security definer set search_path='' as $$
declare customer uuid; result jsonb;
begin
 if auth.uid() is null then raise exception 'NOT_AUTHORIZED'; end if;
 select id into customer from public.customers where auth_user_id=auth.uid() and status='active';
 if customer is null then raise exception 'NOT_AUTHORIZED'; end if;
 select jsonb_build_object('monthlyFee',b.customer_monthly_fee,'currency',b.currency,
 'billingEnabled',b.billing_enabled,'paidUntil',m.paid_until,
 'active',coalesce(m.paid_until>now(),false)) into result
 from public.billing_settings b left join public.whish_customer_memberships m on m.customer_id=customer where b.id=true;
 if result is null then raise exception 'BILLING_SETTINGS_MISSING'; end if;
 return result;
end $$;
revoke all on function public.customer_my_billing_status() from public,anon;
grant execute on function public.customer_my_billing_status() to authenticated;
commit;
