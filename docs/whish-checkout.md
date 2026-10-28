# Whish checkout readiness — updated 19 October 2026

## Verified

The deployed authenticated sandbox flow returned confirmed provider status and persisted WENIK orders for customer USD 3, partner standard statement USD 20 (USD 10 subscription + USD 10 commission on synthetic USD 1,000 sales), and partner trial statement USD 10 (commission only). The user completed each checkout on their phone. These are sandbox payments, not real revenue or membership activation. Independent callback delivery has not been separately established; authenticated return-page status checks work.

Customer success reference: cca6cf0e-269a-4403-866c-79c62ec40219. The three successful orders are in Readiness Test only. Test fixtures are labeled WHISH-TEST and E2E-WHISH. No production schema migration or production deployment was performed.

## Current implementation

- Provider credentials remain server-only. Preview credentials and database configuration are restricted to feature/whish-sandbox.
- Prices and statement balances are quoted on the server. Partner payments must target an owned issued statement. Ordinary customers and partner staff cannot change billing settings.
- Each callback/status check verifies Whish's provider status. A browser redirect alone does not authorize fulfillment.
- Repeated pending creates reuse a link after checking its current status. Verified expired links get a new persisted order. An already confirmed sandbox statement returns its successful order instead of charging again.
- Production customer fulfillment adds one month once per successful order; production partner statement settlement inserts one ledger entry per order. Both branches were tested in isolated PostgreSQL, including duplicate callbacks. Sandbox does neither.
- The payment result now includes its actual kind, amount, currency and invoice reference. Switching away from a result cancels polling and restores the payment button.
- Web customers have a My Membership page; partners can open payment for a specific statement. The mobile ME screen has an account-scoped membership status card.
- customer_my_billing_status checks auth.uid and returns only the caller's fee, expiry and active status. It cannot be called anonymously. Apply sql/whish_customer_billing_status.sql after the base migration.
- Public configuration contains no provider/service secrets. Native checkout is explicitly disabled. The server still rejects live checkout even if an environment flag is accidentally enabled.

## Release blockers

1. Institution paperwork and Whish production credentials/merchant activation are still outstanding.
2. Review and apply the final migrations to production, provision its public configuration, and deploy only after release approval. Production checkout remains disabled.
3. Apply sql/whish_partner_membership.sql after statement checkout. Fully settled subscription-bearing statements now renew once from the later of payment time, existing expiry, and trial end. Commission-only statements never renew. Administrative suspension is preserved. This has passed isolated and hosted rollback tests; production remains untouched.
4. Apply sql/whish_membership_access.sql after membership status. An opt-in private server trigger checks active customer and partner memberships for new confirmed transactions across API versions. It is OFF by default and only the active Super Admin may enable it, with an audit record. Existing confirmed transactions are not retroactively blocked. New points-redemption requests now use the same opt-in membership gate via sql/whish_redemption_access.sql. Previously approved gifts remain collectible even after membership expires. Historical/manual payment treatment still needs rollout review. No production customer status has changed.
5. Apply sql/whish_refund_review.sql after partner membership. Verified refunds now create one review, remain refunded under delayed success, and require an audited Super Admin decision to retain access or set a reviewed expiry. whish-refunds.html supplies that workflow. This does not request refunds from Whish or automatically reverse/credit invoice accounting; an operator must reconcile financial ledger adjustments separately.
6. Resolve native store payment classification before adding a Whish purchase button to a distributed app. Google/Apple distinguish digital app subscriptions from physical goods/services. Institution registration alone does not resolve that classification. Native membership display is ready in source; no new app binary was generated.
7. Whish confirmed by email on 19 October 2026, in response to the recurring debit request, that only Direct Credit and refund functionality are supported. Treat recurring collection as unavailable for this integration. Direct Credit transfers merchant funds to customer wallets and must not be used as subscription collection. Continue with customer-confirmed payments; no scheduled debit exists. Refund API documentation, eligibility and activation requirements are still needed before implementation.

## Validation

JavaScript provider, checkout and public-configuration checks; 30 isolated PostgreSQL checks including authenticated membership privacy and duplicate statement prevention; mobile TypeScript noEmit; syntax checks for the API and changed HTML modules. Hosted Readiness Test verified the new account-scoped status and statement behavior. No production data was used for these tests.

Official policy references reviewed:
- https://support.google.com/googleplay/android-developer/answer/9858738?hl=en
- https://developer.apple.com/app-store/review/guidelines/


## Membership reconciliation update

New service-only whish_statement_memberships ledger grants exactly one month for each fully paid subscription-bearing statement. Partial payment, trial commission and sandbox success do not grant a month. Duplicate provider confirmations cannot extend again. A suspended partner remains suspended even if the paid expiry advances. Test data and production-branch SQL were exercised only in the isolated database, with hosted changes rolled back. The new enforcement switch is false in Readiness Test.

Security advisor reports RLS-without-policy for service-only billing tables (intentional: ordinary clients have no table grants) and authenticated SECURITY DEFINER notices for super-admin settings RPCs. These RPCs explicitly check active super-admin authorization, reject anonymous callers, use a fixed empty search_path, and are covered by negative authorization tests. Review guidance: https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable .


## Refund review and earned gifts

The refund wrapper locks the payment before its review (matching the admin resolver lock order), preserves a terminal refunded status, and never automatically removes later purchased months. Only Super Admin can inspect/resolve reviews or adjust membership expiry. Sandbox reviews cannot change production access. Duplicate callbacks create one review; a resolved review is not reopened by another callback. This is an access-review workflow, not a financial refund API or invoice-credit implementation.

New gift requests require a valid customer membership only when enforcement is enabled. Existing approved redemptions may still be collected after expiry. Hosted rollback verification confirmed refund monotonicity and a single review; all seeded tests were rolled back.

Android and iOS JavaScript/Hermes exports both compiled successfully with isolated public test configuration. These are intermediate bundles, not signed APK/AAB/IPA binaries and not store submissions.

## Manual renewal messaging — 19 October 2026

Customer web billing distinguishes activation from renewal and shows an in-page expiry reminder during the last seven days of an active membership when live checkout is enabled. Sandbox never displays a real renewal reminder. Partner billing explicitly requires confirmation for each statement. These are in-page notices, not push notifications, email, SMS or a scheduled reminder service. Native checkout remains disabled pending store classification. No production release or configuration change is included.

Native membership now refreshes when the ME card gains focus and when the app returns from background, so an external payment can be reflected without restarting. A seven-day in-app expiry notice is shown only for active memberships with billing enabled. No native purchase link or background push service was added.

## Phone retry verification — 19 October 2026

At 16:02 Beirut time, a Customer sandbox checkout for USD 3 completed successfully after retrying an unpaid order. Readiness Test records confirm the previous order b5460aa2-0336-4a20-b7a3-dccef1911ff8 is failed with no fulfillment, and replacement order 4af2bb14-f58a-46e2-ba59-a2d457a4409f is success. Its sandbox fulfillment marker was written at 13:02:49 UTC. No real membership was activated and no live funds were collected.

The old checkout page was observed expired while the stored state was still pending; later provider reconciliation returned failed and displayed Try again. This proves recovery from an unpaid/expired checkout, not independent evidence that the provider's Simulate Failure button immediately reports failed. Keep that distinction in acceptance testing.

The status response now includes normalized providerState separately from persisted state. An unknown provider answer cannot overwrite a previously confirmed order. The result page distinguishes provider pending from inconclusive verification and offers Check payment status after its bounded polling period. That control checks the same order only; it never calls create. A replacement is still allowed only after verified failed status and another server-side reconciliation.

Validation: checkout service 11/11 tests passed, local UI behavior checks covered pending, unknown, successful recheck blocking and failed-order retry; GitHub Whish readiness run 39256263797 passed on commit 73c849ba9eea67e97872407fd31fdf78de3ebd2b. The deployed preview returned HTTP 200 with the new status control. No production release was made.

Partner records were rechecked: the USD 20 standard and USD 10 trial statement sandbox successes from 17 October remain present. The updated partner billing page reads environment-specific public configuration and preserves statement-specific checkout links. Partner retry on the latest preview was subsequently completed and verified as described below. Independent callback delivery, financial refund processing, native store classification and all production gates remain open.

## Partner retry closeout — 19 October 2026

The user completed retry from their phone for statement WHISH-TEST-RETRY-20261019 (statement cf11a7c5-906f-403f-bfd0-c866192beb65), a synthetic USD 20 fixture in Readiness Test only. Both previous orders 16051e4e-8c3c-4960-b698-20154163b85e and 3aba0d12-d13a-4027-acfa-c0a7b655ca90 are failed and have no fulfillment marker. Replacement b2376de5-db88-4e89-9fe0-23ecb485e82e is success for the same statement and amount; its sandbox fulfillment marker was written at 14:09:56 UTC (17:09 Beirut). The return page displayed the expected invoice reference and confirmed USD 20. Read-only database verification matched the screenshot.

The user was initially directed to the already-tested standard statement. Its successful-order guard returned already confirmed without starting a new payment. A fresh WHISH-TEST-RETRY fixture was then created for retry testing; existing fixtures were not reset. Sandbox statement balances deliberately remain unchanged because live settlement is disabled.

Provider pending was observed after the user followed the Simulate Failure flow, and a later verification returned failed. Thus recovery from verified nonpayment is confirmed for customer and partner, but immediate sandbox failure propagation is not established. A transient browser Failed to fetch was recovered by checking the same payment, without forcing its state or bypassing server verification. No production release, real collection, membership activation, refund transfer or manual status override occurred.

The phone retry acceptance cases are complete. Remaining release acceptance is independent callback delivery and verified financial refund handling, followed by institution/merchant activation, reviewed production migrations/configuration and explicit release, plus native store classification and signed builds. Do not repeat phone retry tests without a new failure or material code change.


## Live preparation — 28 October 2026

Whish issued a live channel and separate secret for the exact website header `wenik.co`. Both were saved as production-only sensitive Vercel variables. A read-only merchant balance connectivity request from an ephemeral Vercel sandbox in iad1 returned HTTP 200 with provider status true; no balance was displayed, no collect link was created and no payment was made. The same endpoint returned HTTP 403 from the local workspace, so local failure is not evidence of invalid credentials. The ephemeral sandbox was stopped.

The seven reviewed SQL scripts were compiled in one rolled-back production transaction and then applied as migration `whish_live_checkout_readiness`. Checkout and membership enforcement were initially OFF; no historic payments or expiry dates were changed. All five new tables have RLS enabled and no anon/authenticated table access. A service-role prepare for the owner's existing active customer returned the server-priced USD 3 quote inside a rolled-back transaction.

Production API now requires `WHISH_ENVIRONMENT=production`, Vercel production hosting, `WHISH_CHECKOUT_ENABLED=true` and separate `WHISH_LIVE_CHECKOUT_APPROVED=true`. Public configuration reflects those effective gates. An optional server-only `WHISH_LIVE_ALLOWED_USERS` comma-separated UUID list restricts live creation to the pilot customer until the first real payment is verified. Status and signed callbacks remain available for existing orders. Preview credentials stay sandbox-scoped. Native purchases remain disabled.

Validation: 26 JavaScript checks and 30 isolated PostgreSQL checks passed. The new API tests verify that no flag combination enables live payments on previews and that nonpilot users cannot create a live charge. Actual live checkout, independent callbacks, user-confirmed payment and membership fulfillment must still be verified on the final deployment. Refund transfer/ledger reversal is not implemented; verified refunds enter Super Admin review.


## First live customer payment — 28 October 2026

The user confirmed debit from their Whish wallet and receipt in the company wallet. Read-only WENIK verification matched one production customer payment for USD 3, state success, fulfilled at 12:16:29 UTC, with paid_until 28 November 2026 at 12:16:29 UTC. This confirms live collection reported by the user and persisted membership fulfillment; it does not independently prove callback delivery or test partner payment/refund transfer.

The customer website now shows a membership card immediately after sign-in. Active customers see their expiry and a View Membership link; inactive customers see the server-configured fee and Activate & Pay. The Me section retains a clearly labeled payment link. Returning to the website refreshes the card. The service worker no longer caches /api responses or serves old payment verification responses offline. Native purchase links and membership enforcement remain off.


## Customer membership and QR access — 28 October 2026

User approved open browsing with paid membership required for QR benefits, earning points and new gift reservations. A separate customer_membership_required setting keeps this customer requirement independent of partner membership enforcement. QR refresh and all three legacy/current partner QR lookup RPCs verify paid access; all lookup versions also require the QR expiry to remain valid. Unpaid profiles retain browsing access but return no QR token. New confirmed transactions and new points gift requests enforce the same server check. Existing approved gifts remain collectable and historical confirmed transactions remain editable.

The customer website clears any old QR before verification, offers Activate Membership when unpaid, and refreshes after returning from payment. QR display expires at the earlier of token or membership expiry. Failed verification clears a stale QR. Native RPCs share the server restriction, but this update does not build a new native binary or add a native payment link.

Validation: three UI behavior checks passed for paid, unpaid and failed verification. Hosted production-schema tests ran in a rolled-back transaction: paid QR/profile allowed; expired QR/profile denied; new transactions and gift requests denied after expiry; approved gifts collectable; ordinary customer cannot alter the requirement. The public catalog and partner browsing RPCs were not changed.
