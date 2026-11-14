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
1. Run the included integration suite on a fresh PostgreSQL database in GitHub Actions.
2. Repeat dependency audit in CI on the pinned requirements. Local scan reported no known vulnerabilities; this does not establish overall application security.
3. Complete mobile browser QA for each role, error states, password changes and deactivation.
4. Replace in-memory login rate limiting with shared persistent limiting before scaling.
5. Add versioned schema migrations, restore-tested backups and monitoring before real use.
6. Review role matrix with owner: owner/manager/chef/accountant/buyer have network scope;
   souschef/bar are restricted to one restaurant. Do not infer per-employee assignments.
7. Review TLS, correct hostnames and private-service connectivity on Render.
8. Independent security review before enabling public access or onboarding real employees.

No real employee data, passwords, contacts or payroll are included. Synthetic credentials in
CI/tests are for disposable test databases only. Do not reuse them on a live service.
The financial module remains out of scope for this version; there is no accounting ledger.

Render config is a PRIVATE service, not a public web service. Auto-deploy is off and the
release gate is false. Creating a Blueprint can allocate paid resources and trigger its first
build even when auto-deploy is off; do not create it until reviewed. No resources were created.
