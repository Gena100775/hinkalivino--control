# Security review — 2026-11-15

Status: staging preparation; NOT approved for public or real-employee use.

## Implemented and tested locally
- Argon2id password hashes; random bearer sessions stored hashed, with 8-hour expiration.
- Server-side role and restaurant checks; owner-only user creation/listing/deactivation.
- Password changes and deactivation revoke all affected sessions.
- Assigned-role/supervisor checks for task completion.
- Login failure throttle, generic credential errors and dummy hash for missing users.
- Parameterized SQL, escaped UI strings, no browser token persistence, no-store responses.
- PostgreSQL row locks for receipts/inventory; receipt state prevents duplicate stock credits.
- Security headers and allowed-host checks. PostgreSQL required in production.
- Deployment startup blocked unless HV_RELEASE_APPROVED=true in production.

## Release gates still open
1. PostgreSQL 16 integration suite passed in GitHub Actions for c0824fda; rerun after application changes.
2. Dependency audit passed in CI on the pinned requirements; this does not establish overall application security.
3. Complete mobile browser QA for each role, error states, password changes and deactivation.
4. Replace in-memory login rate limiting with shared persistent limiting before scaling.
5. Add versioned schema migrations, restore-tested backups and monitoring before real use.
6. Review role matrix with owner: owner/manager/chef/accountant/buyer have network scope;
   souschef/bar are restricted to one restaurant. Do not infer per-employee assignments.
7. Verify TLS to Neon, least-privilege database access, exact Render hostname and a separate synthetic-data database branch.
8. Independent security review before enabling public access or onboarding real employees.

No real employee data, passwords, contacts or payroll are included. Synthetic credentials in
CI/tests are for disposable test databases only. Do not reuse them on a live service.
The financial module remains out of scope for this version; there is no accounting ledger.

Render config now plans a FREE public-network web service, with Neon Free PostgreSQL.
The former paid private-service plan was never approved. No Render compute or database was
created. Free public ingress must not be confused with internal-only private hosting.
Auto-deploy is off and the production release gate remains false. Planning is safe; approving
and applying the Blueprint can start deployment. Do not approve it until the security review
and user approval of the reviewed deployment plan are complete. Do not use real employee data.
