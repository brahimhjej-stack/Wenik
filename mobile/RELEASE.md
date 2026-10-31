# WENIK Android and Apple release preparation

## Preserve the existing application

- Source of the current customer UI: `mobile-app` (not the older mobile copy on `main` or `feature/whish-sandbox`).
- Expo owner / slug: `wenik` / `wenik`.
- EAS project: `0e651e5b-3660-43c0-8329-5fc0269ff725`.
- Android application ID and iOS bundle ID: `com.wenik.app`.
- Official icon remains `../wenik-logo-final.png`.

Do not create another Expo project, rotate signing keys, or replace the customer UI with the payment branch. Port any later membership changes selectively after comparing both branches.

## Evidence as of 25 October 2026

GitHub Actions run [37673885364](https://github.com/brahimhjej-stack/Wenik/actions/runs/37673885364) completed the Android production AAB build step successfully on 7 October. It waited for EAS (no `--no-wait`). The run has no GitHub artifact; recover the downloadable AAB from the existing EAS project. This is not evidence of Play approval, publication, or a current device test.

No signed iOS build or App Store Connect enrollment/status was verified in this review. Existing Apple account ownership, active developer membership, signing certificate/provisioning profile, and the app record must be checked in the actual account before claiming TestFlight readiness.

## Local validation (no paid build)

```sh
cd mobile
npm ci --ignore-scripts
npm run export:native
npx expo export --platform web --output-dir dist
```

Android/iOS Hermes exports validate JavaScript bundling; they are not APK/AAB/IPA files and cannot replace signed native builds or device checks. The mobile check workflow now includes native exports as well as web export.

## Explicit build commands

```sh
npm run build:android:apk
npm run build:android:production
npm run build:ios:production
npm run build:ios:simulator
```

- `preview`: internal test distribution; Android APK, iOS requires configured device provisioning.
- `production`: Android AAB or signed iOS store build, suitable for subsequent Play/TestFlight upload. It does not submit automatically.
- `ios-simulator`: iOS simulator build, not installable on a physical iPhone or submittable to the App Store.

The manual **WENIK Android and Apple build** workflow builds the selected ref with the existing `EXPO_TOKEN` repository secret. It waits for completion and deliberately has no auto-submit step. First-time iOS credential setup must be completed through Expo/Apple's authenticated flow; non-interactive builds cannot invent the required credentials. A build may consume EAS quota: no cloud build was launched as part of this preparation.

## Remaining account and release gates

1. Retrieve and identify the existing Android AAB/version before scheduling another paid build.
2. Verify Apple Developer enrollment, team, signing credentials and the `com.wenik.app` App Store Connect record; then build and test through TestFlight.
3. Review the current Google Play correspondence. Institution paperwork completing on 28 October does not itself establish Play approval.
4. Resolve store payment classification before introducing a Whish payment action in either native app. Preserve the existing no-checkout native behavior meanwhile.
5. Confirm privacy/account-deletion pages and store declarations against actual app data collection; complete metadata and genuine device screenshots.
6. Run native checks for startup, auth persistence, QR and location permission behavior on Android and iPhone. Prior customer acceptance is retained; only native-specific or changed behavior needs repeating.
7. Submit to internal testing/TestFlight before requesting public release. Production deployment, live payment enablement and store submission are separate steps.


## Membership display update — 31 October 2026

The current native Home screen and Me page now use the account-scoped customer_my_billing_status RPC. Home places the membership card after the hero and View Membership opens Me. Both cards show the configured monthly price, paid expiry and active status. App foreground and explicit refresh reload the same database record as the website; the Home refresh control refreshes membership too. No browser storage or anonymous profile determines paid access.

The Android APK workflow now builds its existing preview profile (installable APK), matching the workflow name, instead of a store-only AAB. Store production AAB and iOS build profiles remain available through the manual build workflow. This change does not submit to either store or add native Whish checkout.

Validation for this update: Android and iOS Hermes exports succeeded; TypeScript compiler and React type dependencies are now declared and the Expo tsconfig is committed. The pre-existing duplicate heroSub style entry in Wins was removed while retaining the final effective style. No live database or web release changes are included.
