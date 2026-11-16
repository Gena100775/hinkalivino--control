# Hinkali & Vino Control 0.5

Recovered from the existing v0.4 package, not rewritten from scratch.
FastAPI + SQLAlchemy + PostgreSQL; local SQLite support. Russian mobile-friendly interface.

## Features
- Employee login and personal cabinet with password change.
- Owner management of employee accounts, roles, restaurant scope and activation.
- Restaurants: Мясницкая, Таганская, Неглинная.
- Purchase requests, delivery/receipt, stock counts, tasks and audit trail.
- Seven roles: owner, manager, chef, accountant, souschef, bar, buyer.
- No real employee records and no working financial ledger/POS integration.

## Local start
Python 3.12+:

```sh
pip install -r requirements.txt -r requirements-dev.txt
# Set HV_ADMIN_PASSWORD to your own unique 16+ character password in the environment.
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --workers 1
```

First startup creates the `owner` account using HV_ADMIN_PASSWORD; there are no default
employee passwords. `.env.example` documents variables; `.env` is not loaded automatically.
Database tables are created on startup; existing v0.4 tables remain compatible.
Run `python -m pytest -q` on a disposable database only.

## Verification
- Local suite: 3 tests passed on SQLite, including authorization, stock workflow,
  task restrictions, password/session revocation, deactivation, host validation and throttling.
- Dependency scan (`pip-audit`): no known vulnerabilities reported by the advisory service.
- Python syntax compilation and JavaScript `node --check`: passed.
- GitHub Actions PostgreSQL 16 integration tests and dependency audit passed on commit c0824fda4307adacbf575a664a5d255e418e0f1f.
- Browser QA and Render runtime verification remain pending. See SECURITY.md.

## GitHub and Render
Target: https://github.com/Gena100775/hinkalivino--control

GitHub connection verified for Gena100775. Source is uploaded to the review branch
`staging/v0.5-security`. No application has been deployed. Never force-push remote history.

`render.yaml` now plans Render Free in Frankfurt, with Neon Free for PostgreSQL.
The Neon project has been verified in aws-eu-central-1 on its Free plan.
DATABASE_URL must be supplied through the Render secret environment, with TLS and preferably
a pooled connection. Never commit or print credentials. Create a separate test branch/database
on Neon before schema initialization; leave the default branch untouched.

No Render web service or deployment has been created. The previous paid/private plan was not
approved. The free service would have a PUBLIC network address after deployment; authentication
does not make it a private service. Auto-deploy is off and HV_RELEASE_APPROVED=false blocks
startup. Security review and explicit approval of the reviewed deployment plan are still required.

Render Free sleeps after 15 idle minutes and has usage quotas. Neon Free has storage/compute
quotas and scale-to-zero. Keep accounts on Free and do not add billing for this test.
Free plans are for synthetic-data testing, not live restaurant operations.

Render specification: https://render.com/docs/blueprint-spec

## Security staging update 0.5.1

Login budgets now persist in PostgreSQL, browser JS uses external files under a stricter CSP,
and startup can run without database schema privileges. `HV_SCHEMA_MANAGED=true` verifies
schema version 1 and skips DDL. Apply migrations/001_initial.sql as the database owner first;
use a database-scoped read/write role for runtime. Keep secrets out of Git and chat.
The exact release commit must pass CI before enabling synthetic-data staging. See SECURITY.md.
