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
- PostgreSQL CI workflow prepared with PostgreSQL 16; not yet executed on GitHub.
- Browser QA and Render runtime verification remain pending. See SECURITY.md.

## GitHub and Render
Target: https://github.com/Gena100775/hinkalivino--control

GitHub connection verified for Gena100775. Source is uploaded to the review branch
`staging/v0.5-security`. No application has been deployed. Never force-push remote history.

`render.yaml` prepares a private PostgreSQL-backed staging service with external database
access disabled, auto-deploy off, and HV_RELEASE_APPROVED=false. It is intentionally blocked
from starting before the security gates are cleared. No Render resources were created.

After review: connect repository in Render, verify current pricing, inspect Blueprint changes,
configure strong HV_ADMIN_PASSWORD and exact HV_ALLOWED_HOSTS, then explicitly clear the
release gate. Keep staging private. Public access is a separate release decision.
Render specification: https://render.com/docs/blueprint-spec
