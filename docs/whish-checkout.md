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
3. Partner invoice settlement and partner access renewal currently use separate legacy models. Define and implement how a fully settled calendar-month invoice advances access; do not grant a month again for a duplicate or commission-only trial invoice.
4. Customer membership expiry is recorded separately; existing app entitlement/access checks need to consume it before a paid launch. No existing customer status has been changed.
5. Refund/credit handling records provider refund status but does not automatically reverse or credit access. It needs an explicit business policy and reconciliation workflow.
6. Resolve native store payment classification before adding a Whish purchase button to a distributed app. Google/Apple distinguish digital app subscriptions from physical goods/services. Institution registration alone does not resolve that classification. Native membership display is ready in source; no new app binary was generated.
7. Automatic renewal is not implemented. The user confirms a follow-up email has been sent to Whish; await recurring mandate/debit API documentation and explicit customer consent requirements. No scheduled debit exists.

## Validation

JavaScript provider, checkout and public-configuration checks; 18 isolated PostgreSQL checks including authenticated membership privacy and duplicate statement prevention; mobile TypeScript noEmit; syntax checks for the API and changed HTML modules. Hosted Readiness Test verified the new account-scoped status and statement behavior. No production data was used for these tests.

Official policy references reviewed:
- https://support.google.com/googleplay/android-developer/answer/9858738?hl=en
- https://developer.apple.com/app-store/review/guidelines/
