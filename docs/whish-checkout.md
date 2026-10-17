# Whish checkout readiness — 17 October 2026

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
7. Automatic renewal is not implemented. The user confirms a follow-up email has been sent to Whish; await recurring mandate/debit API documentation and explicit customer consent requirements. No scheduled debit exists.

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
