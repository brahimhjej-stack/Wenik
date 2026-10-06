do $permissions$
declare f record;
begin
 for f in select p.oid::regprocedure signature from pg_proc p where p.pronamespace='public'::regnamespace and (p.proname like 'admin_finance_%' or p.proname in ('admin_add_finance_transaction','admin_reverse_finance_transaction')) loop
  execute format('revoke execute on function %s from public, anon',f.signature);
  execute format('grant execute on function %s to authenticated',f.signature);
 end loop;
 for f in select p.oid::regprocedure signature from pg_proc p where p.pronamespace='public'::regnamespace and p.prorettype='trigger'::regtype loop
  execute format('revoke execute on function %s from public, anon, authenticated',f.signature);
 end loop;
end $permissions$;