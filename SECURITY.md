# Security review — 2026-11-16

Scope: synthetic-data staging only. This is not approval for real employee data or production accounting.

Implemented:
- Argon2id passwords and random bearer sessions; only token hashes are stored in PostgreSQL.
- Eight-hour session expiration; logout, password changes and deactivation invalidate sessions.
- Server-side restaurant and role checks; owner-only employee administration.
- Database-backed login request budgets (20 per IP and 40 per account in 15 minutes), atomic
  increments, and bounded concurrent password verification. Successful login does not reset budgets.
- Parameterized SQL; PostgreSQL row locks prevent duplicate receipts; inventory and receipts
  share restaurant locks. Supplier buyers cannot perform final receipt.
- Separate JS/CSS assets; script CSP allows same-origin files only; user strings are escaped.
- Validation errors exclude submitted field values. No browser localStorage/sessionStorage tokens.
- Exact Render hostname allowlist, no-store, frame denial, permissions and referrer policies.
- Versioned initial schema in migrations/001_initial.sql. Managed startup verifies schema version
  and avoids DDL; application runtime must use a scoped read/write database role.
- HV_RELEASE_APPROVED=false prevents startup before database access, verified by regression test.

Checks:
- Local authorization/workflow tests passed on disposable SQLite; concurrency test is PostgreSQL-only.
- Initial schema applied successfully to isolated Neon QA branch on PostgreSQL 18.
- Dependency audit reported no known vulnerabilities. This does not establish absence of flaws.
- GitHub CI targets PostgreSQL 16/18; results must pass for the release commit.
- Local browser QA could not connect to the container's localhost; no browser pass is claimed.

Staging release procedure:
1. Require passing CI for the exact commit; run migration on the isolated staging database.
2. Use a read/write runtime role, TLS connection, one server process, Free plan and auto-deploy off.
3. Only after code/security checks above pass, enable a synthetic-data staging run to verify
   actual browser login, role visibility and workflows. Keep real employees and business records out.
4. Do not call a service usable until HTTPS health, unauthenticated access denial and browser
   behavior are checked. If runtime/browser checks fail, restore the gate.

Before real operational use: independent security review, restore-tested backups, data retention
and privacy review, MFA/account recovery, audit pagination, monitoring, request-size/load testing,
and an approved role matrix. Finance/POS integrations and accounting ledger are not implemented.
Free web service ingress is PUBLIC even though application routes require login.
No production or real-employee approval is implied by a green test suite.
