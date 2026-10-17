# Whish checkout — sandbox implementation

Prepared against Whish Pay v1.4.4 documentation supplied by Whish, and the current production database schema (read-only inspection). Defaults use billing_settings: customer $3/month, partner $10/month; existing partner trial dates are retained. New partner trial end is based on partner creation plus 3 calendar months, so checkout does not restart a trial.

## Required before deployment

Apply sql/whish_checkout.sql to an isolated test database and validate it there. Set server-only variables SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, WHISH_CHANNEL, WHISH_SECRET, WHISH_WEBSITE_URL (exact issued value), WHISH_SITE_URL (public HTTPS origin), WHISH_CALLBACK_SECRET (random 32+ characters), WHISH_ENVIRONMENT=sandbox, WHISH_CHECKOUT_ENABLED=true. Enable the database checkout switch using whish_update_settings from a signed-in active super admin.

Never commit credentials. The test credentials were checked against the sandbox balance endpoint successfully on October 17, 2026. No real payments were taken. Validation completed: 13 JS tests plus 11 local SQL scenario checks passed. Vercel project `wenik` has SMS secrets but no SUPABASE_SERVICE_ROLE_KEY configured; a secure server-side database credential is still required for deployment. Never paste it in chat.

The new page /whish-payment.html is sandbox-only. No link is added to production navigation. API handlers explicitly reject production mode until review.

## Verification

Run `node --test tests/whish*.test.js tests/whish-sql.test.mjs`. The local isolated PostgreSQL tests use the pinned PGlite dev dependency and mocked copies of the inspected WENIK tables; they do not mutate the hosted database. Then test wrong OTP, pending, correct OTP, duplicate callback, concurrent callbacks, missing callback/status polling, changed prices mid-payment, customer/partner isolation and trial exemption with Whish's documented sandbox values. A checkout redirect is not proof of payment. Unknown/500 outcomes must be reconciled using the same persisted externalId.

## Remaining production work

- Apply and verify SQL in a test database, then explicitly review the production migration.
- Deploy server secrets and callback routes; verify an actual successful sandbox checkout.
- Verify entitlements are respected by current app access checks; customer membership expiry is stored separately and does not overwrite customer status.
- Verify partner payment ledger integration and refund entitlement handling; refunded orders are recorded but require manual review for access reversal.
- Test the added super-admin guards on the existing billing settings, partner payment and statement payment tables with the live-schema test environment before production.
- Obtain Whish recurring-payment mandate API documentation before adding automatic debit. No automatic debit or mandate is claimed or scheduled.

This draft is not a production-ready payment launch.

## Partner statement checkout (October 17 update)

Partner payment now requires a selected issued monthly statement. The server quotes its remaining balance (subscription + sales fee + authorized adjustments minus payments), rather than collecting a separate $10 subscription. The existing statement generator charges the sales fee from the start; only the subscription is waived during the first three months. Existing statement rounding/fractional waivers and complimentary dates are retained.

Apply `sql/whish_statement_checkout.sql` after the base script. Both migrations were applied to WENIK Readiness Test only; production SQL is unchanged. Statement payments get a unique Whish order reference, preventing duplicate ledger settlement. Sandbox confirmation never pays a real invoice. Super-admin guards also cover statement adjustments. Customer checkout remains $3 monthly.

Vercel production configuration now contains the server credentials, with checkout explicitly disabled. Secret values were not inspected. No redeploy, live payment, automatic debit, or production migration was performed. Validation: 14 JavaScript tests and 16 isolated SQL checks passed; hosted test metadata verified service-only RPC permissions. A hosted transactional fixture attempt returned an expired connector request, so hosted financial settlement is not yet verified. Remaining work includes real sandbox checkout/callback verification, partner access renewal policy for settled invoices, and refund/credit reconciliation.

## Verified payment and database results (October 17, 2026)

Whish sandbox status API confirmed `success` after the user completed both the $3 customer checkout and the $20 partner example ($10 subscription + $10 fee). These were provider-only requests; their callbacks were not linked to persisted WENIK orders, and neither proof constitutes a deployed browser-to-API-to-database test.

Separate rollback-only tests on hosted WENIK Readiness Test verified: combined $20 statement preparation, sandbox isolation under duplicate success, exactly one ledger payment and paid invoice under the production reconciliation branch, and exactly one month customer renewal for a $3 order under duplicate success. No production database or real financial account was modified. The isolated schema had no billing_settings row; the customer fixture supplies $3/$10/1%, and prepare_order now explicitly rejects missing billing configuration. Checkout remains disabled. Public callback delivery, authenticated checkout from the deployed test page, partner access enforcement, and refunds still need verification.
