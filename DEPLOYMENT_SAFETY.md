# WENIK Deployment Safety

## Goal
Keep production stable while allowing continuous development.

## Branches
- `main`: production branch. Do not edit directly for feature work.
- `staging`: all new work starts here and should create Vercel Preview deployments.

## Release flow
1. Make changes on `staging`.
2. Test the Vercel Preview on mobile and desktop.
3. Check core flows: Join, Login, Home, QR, Partners, Rewards/Gifts, IZA, Customer, Admin.
4. Check runtime/build errors.
5. Merge to `main` only after the preview is verified.
6. If production breaks, use Vercel Instant Rollback to the last known-good production deployment.

## Sensitive areas
Extra review/testing is required for:
- Authentication and account linking
- Database/schema changes
- Finance / P&L
- Cashback balances and settlement
- Gift inventory and draw logic
- Notifications and SMS

## Rule
No direct production edits for normal feature work. Production should only receive tested, reviewed changes from `staging`.
