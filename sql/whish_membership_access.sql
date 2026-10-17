-- Opt-in server enforcement for new confirmed transactions only.
-- Keep OFF until production membership and payment rollout is approved.
begin;
alter table public.whish_checkout_settings add column enforce_member_access boolean not null default false;
create schema if not exists whish_private;
revoke all on schema whish_private from public,anon,authenticated;
create function whish_private.guard_transaction_membership() returns trigger
language plpgsql security definer set search_path='' as $$
begin
 if not coalesce((select enforce_member_access from public.whish_checkout_settings where id=true),false) then return new; end if;
 if new.status<>'confirmed' then return new; end if;
 -- Existing confirmed records remain editable without retroactive re-billing.
 if tg_op='UPDATE' then
  if old.status='confirmed' and old.customer_id=new.customer_id and old.partner_id=new.partner_id then return new; end if;
 end if;
 if not exists(select 1 from public.customers c join public.whish_customer_memberships m on m.customer_id=c.id where c.id=new.customer_id and c.status='active' and m.paid_until>now()) then raise exception 'CUSTOMER_MEMBERSHIP_REQUIRED'; end if;
 if not exists(select 1 from public.partners p join public.partner_subscriptions s on s.partner_id=p.id where p.id=new.partner_id and p.status='active' and s.status<>'suspended' and greatest(s.trial_ends_at,s.paid_until)>now()) then raise exception 'PARTNER_MEMBERSHIP_REQUIRED'; end if;
 return new;
end $$;
revoke all on function whish_private.guard_transaction_membership() from public,anon,authenticated;
create trigger whish_transaction_membership before insert or update of customer_id,partner_id,status on public.transactions for each row execute function whish_private.guard_transaction_membership();

create function public.whish_set_membership_enforcement(p_enabled boolean) returns void
language plpgsql security definer set search_path='' as $$
begin
 if auth.uid() is null or not public.is_wenik_super_admin() then raise exception 'NOT_AUTHORIZED'; end if;
 if p_enabled is null then raise exception 'INVALID_SETTINGS'; end if;
 update public.whish_checkout_settings set enforce_member_access=p_enabled,updated_at=now() where id=true;
 insert into public.audit_logs(actor_auth_user_id,actor_role,action,entity_type,entity_id,payload)
 values(auth.uid(),'super_admin','membership_enforcement_changed','whish_checkout_settings','true',jsonb_build_object('enabled',p_enabled));
end $$;
revoke all on function public.whish_set_membership_enforcement(boolean) from public,anon;
grant execute on function public.whish_set_membership_enforcement(boolean) to authenticated;

-- One transaction for the admin form: a failure rolls back every setting.
create function public.whish_save_settings(p_customer_fee numeric,p_partner_fee numeric,p_enabled boolean,p_trial_months integer,p_enforce_membership boolean)
returns void language plpgsql security invoker set search_path='' as $$
begin
 perform public.whish_update_settings(p_customer_fee,p_partner_fee,p_enabled,p_trial_months);
 perform public.whish_set_membership_enforcement(p_enforce_membership);
end $$;
revoke all on function public.whish_save_settings(numeric,numeric,boolean,integer,boolean) from public,anon;
grant execute on function public.whish_save_settings(numeric,numeric,boolean,integer,boolean) to authenticated;
commit;
