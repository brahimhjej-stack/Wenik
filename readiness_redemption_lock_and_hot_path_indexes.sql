CREATE OR REPLACE FUNCTION public.customer_request_points_redemption(p_prize_id uuid)
 RETURNS uuid
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
declare v_customer uuid; v_cost int; v_balance int; v_partner uuid; v_id uuid; v_qty int; v_used bigint;
begin
  select id into v_customer from public.customers where auth_user_id=auth.uid() limit 1;
  if v_customer is null then raise exception 'CUSTOMER_NOT_FOUND'; end if;

  select rc.points_cost,p.partner_id,p.quantity into v_cost,v_partner,v_qty
  from public.points_reward_catalog rc
  join public.prizes p on p.id=rc.prize_id
  where rc.prize_id=p_prize_id and rc.is_active=true
    and (p.expires_at is null or p.expires_at>=now())
  for update of rc,p;
  if v_cost is null then raise exception 'REWARD_NOT_AVAILABLE'; end if;

  select
    (select count(*) from public.winners where prize_id=p_prize_id and status::text<>'cancelled') +
    (select count(*) from public.points_redemptions where prize_id=p_prize_id and status in ('pending','approved','collected'))
  into v_used;
  if v_used>=v_qty then raise exception 'REWARD_SOLD_OUT'; end if;

  -- Serialize spending across different prizes for the same customer.
  perform 1 from public.customers where id=v_customer for update;
  select coalesce(sum(points),0)::int into v_balance from public.points_ledger where customer_id=v_customer;
  if v_balance < v_cost then raise exception 'NOT_ENOUGH_POINTS'; end if;

  insert into public.points_redemptions(customer_id,prize_id,partner_id,points_cost)
  values(v_customer,p_prize_id,v_partner,v_cost) returning id into v_id;
  insert into public.points_ledger(customer_id,partner_id,entry_type,points)
  values(v_customer,v_partner,'redeem_hold',-v_cost);
  return v_id;
end $function$;

revoke execute on function public.wenik_award_transaction_points(uuid) from public, anon, authenticated;
create index if not exists wenik_points_ledger_customer_idx on public.points_ledger(customer_id);
create index if not exists wenik_redemptions_prize_status_idx on public.points_redemptions(prize_id,status);
create index if not exists wenik_redemptions_customer_idx on public.points_redemptions(customer_id);
create index if not exists wenik_benefits_partner_created_idx on public.partner_benefits(partner_id,created_at desc);
