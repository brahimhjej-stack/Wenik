# WENIK readiness verification — 2026-10-06

Status: partial readiness. No certification of thousands of concurrent users, real-device behavior, automatic payments, or recoverable production backups.

## 1. Isolated scale and concurrency tests
- Created free test project `ccvrfxyshagmtcwqqsoi`, separate from production `zkrnzwnbdoaqanqzznlw`. Branching required Pro, so no paid branch or upgrade was made.
- Restored production schema metadata only: 42 tables, RLS enabled on all 42, function definitions, indexes, policies and grants. No production customer data copied. Production counts rechecked after tests: 9 customers, 13 partners; synthetic accounts/invoices confined to test project.
- Seeded 10,000 synthetic customers and 2,000 synthetic partners; test auth records are artificial and no SMS/email was sent.
- Public directory load: 1,000 HTTP requests, concurrency 25; 1,000 successful, zero errors, 329.89 seconds. Remote client p50 8,046 ms, p95 10,162 ms. Each legacy call returned only 1,000 rows.
- Test-project edge logs indexed at review time: 777 directory requests, zero non-200 responses; origin p50 284 ms, p95 575.6 ms; upstream p95 254.4 ms. This is a partial log sample, not all 1,000 requests. Client timings include substantial remote network overhead.
- Higher read-load stage: 500 HTTP requests, concurrency 100; 500 successful, zero errors, 62.72 seconds. Remote p50 12,134 ms, p95 15,299 ms. This increased client latency must not be presented as a fast end-user experience.
- Fixed the directory row-cap bug in web and actual mobile-app branch: ordered pages of 500, shared short-lived request caching; web renders 24 cards then Show More. Verified actual supabase-js client returns all 2,000 unique partners. Rendering checks passed: initial 24 cards, Show More 48, search finds partner 1999 and changing filters resets visible count.
- 20 concurrent gift requests, same customer with 15 points, two gifts costing 10 each: exactly one redemption, balance 5. No negative balance.
- 20 authenticated customers competing for a gift with stock 1: exactly one redemption, no oversell.
- 20 concurrent invoice calls against one QR with different idempotency keys: exactly one invoice and one earn entry, 40 points. Other calls rejected consumed QR.
- Added 1,000 synthetic invoices via SQL: 1,001 total invoices and 1,001 earn entries. Bulk SQL is not an HTTP write-throughput benchmark.
- This does not represent 10,000 active sessions or 1,000 simultaneous users. Mixed workload and long soak tests remain.

## 2. Customer and partner journey
- Prior rollback checks: insufficient points, inactive customer, sold out, exact debit/refund, duplicate refund and collection rejected; RLS isolation and admin permission checks passed.
- Protected customer fields cannot be edited by ordinary customers; permitted name update and privileged QR refresh passed.
- Points web client/session deadlock and duplicate-client fixes deployed.
- Database-side QR invoice and gift concurrency passed in isolated project.
- Real SMS OTP delivery and a signed-in browser journey on physical devices have not been verified. No real paid transaction generated.

## 3. Native applications
- Actual native build source is `mobile-app`, not the older mobile directory on main. Existing OTP and password recovery preserved.
- Fixed stuck authentication loading state after exceptions, overlap/stale QR display and app-resume QR refresh, and added WhatsApp Contact Us to Me: `https://wa.me/96176468506`.
- Fixed native PNG icon path, Expo Android navigation configuration, RN version compatibility and removed local eas-cli dependency. Added package lock.
- Expo Doctor: 18/18 passed. Final web, iOS and Android JavaScript/Hermes bundle exports passed, including pagination changes.
- GitHub Mobile Check passed for initial mobile fixes; pagination Mobile Check also passed: https://github.com/brahimhjej-stack/Wenik/actions/runs/37517587666
- Android AAB EAS build is asynchronous and was still running at report time. JavaScript export does not prove APK/AAB or IPA installation success.
- Physical iPhone/Android camera, QR scanning, background/resume, notification permissions and full login/redemption journeys remain unverified. Native system push notifications are not currently implemented in this branch; inbox messages are separate.

## 4. Monitoring and recovery
- Availability workflow runs every 15 minutes on GitHub, checks production website and public partner RPC without writes. First workflow run succeeded: https://github.com/brahimhjej-stack/Wenik/actions/runs/37516803643
- Follow-up production checks succeeded (both HTTP 200).
- Latest web pagination deployment READY on Vercel: `dpl_4ktjNvZmiWwQewwqSbeyJhsqfB1U`.
- Schema reconstruction succeeded in test project. This is NOT a production data backup or disaster restore test.
- Production backup availability, retention, off-site database exports, Storage object backup and full recovery drill remain unverified. Current free plan cannot be assumed to provide daily recoverable backups. No paid backup/PITR option enabled.
- GitHub Actions failure notifications depend on account settings; no WhatsApp/SMS incident alerts configured.

## 5. Billing and payments
- Production billing configuration: customer $3/month, partner $10/month, commission 1%, due day 5, USD, Asia/Beirut.
- Partner subscription confirmation rollback test passed: extension once, duplicate Whish reference blocked, duplicate extension prevented. All financial test changes rolled back.
- Existing flow supports manual confirmation with method Whish; this does not establish automatic Whish settlement or payment callback verification.
- Provider sandbox/API access, signed callback integration and end-to-end $3 customer subscription collection remain blockers. No provider charge made.

## Release gates
1. Real SMS and physical iOS/Android end-to-end tests.
2. Successful native binaries installed and exercised; native push if required for launch.
3. Verified recoverable database and Storage backups with off-production restore.
4. Whish sandbox settlement/refund and subscription lifecycle, or explicitly agreed manual collection process.
5. Mixed read/write soak, incremental higher concurrency, resource/connection metrics and agreed response targets.

Repository commits: native hardening `0863ef02951b828d6bb373f2e88e4eaa863dcb9d`; availability `5765839df858aca3c45c84fb995a13b6074939a1`; web directory `af07cd6909796a8a412269d44b5b701e03f3c055`; native directory `5c51aa6d4927c8b0f3e009a79dc0f6ad9fc438ca`.
