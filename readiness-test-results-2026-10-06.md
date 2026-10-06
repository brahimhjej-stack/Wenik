# WENIK readiness verification — 2026-10-06
## Passed
- Public partner RPC: 20 requests / concurrency 5, 20 successful; p50 8013 ms, p95 9698 ms.
- Public partner RPC: 40 requests / concurrency 10, 40 successful; p50 6518.5 ms, p95 7712 ms.
- Timings include remote network/TLS overhead; these are not database-only timings.
- All public ordinary tables have RLS enabled.
- Current dataset: 9 customers and 13 partners. Duplicate earn entries: 0; negative customer ledger balances: 0; invalid redemption costs: 0.
- Customer protected-field guard: authenticated non-admin update to mobile_verified rejected, name update allowed, privileged QR refresh works. Entire test rolled back.
- Live customer page loads and rejects empty login fields.
- Points module loaded once after deployment c9a5f63ea393329f20d4d99c78ea683a05a99970.
- Points requests now start only with authenticated session and refresh on sign-in/session changes.
## Limitations / remaining checks
- This does NOT certify thousands of concurrent users.
- No isolated development database exists; only main branch is available.
- No heavy production write load, real SMS or paid transactions generated.
- Logged-in browser customer/partner/admin full journey not verified.
- Actual simultaneous redemption race test not yet executed.
- Native iOS/Android build not tested in this session.
- Customer Supabase client consolidated; fresh-browser logs show no multi-client warning.
- Large realistic dataset, mixed read/write load, p95 targets, connection pool and monitoring need validation before broad rollout.

## Follow-up verification
- Public website burst: 20 requests / concurrency 5; all successful. p50 7520 ms, p95 10165 ms (network included).
- Gift rollback flow passed: insufficient points rejected, inactive customer rejected, exact debit verified, sold-out gift rejected, refund restores exact balance, repeat refund blocked, approved gift collection succeeds and second collection blocked.
- Customer RLS isolation passed: no other customers or other balances readable; admin approval forbidden to non-admin customer.
- No fixture changes persisted: all database functional tests use BEGIN / ROLLBACK.
