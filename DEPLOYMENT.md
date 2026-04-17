# Deployment Guide

## 1) Production prerequisites
- Python 3.11+
- Managed PostgreSQL database
- Public HTTPS domain (or managed platform URL)
- Environment variables configured securely (no `.env` committed)

## 2) Required environment variables
- `DATABASE_URL` (PostgreSQL for production)
- `OPENROUTER_API_KEY` (optional, enables advanced LLM chat)
- `OPENROUTER_MODEL` (optional)
- `WEATHER_API_KEY` (optional)
- `MARKET_DATA_API_KEY` (recommended for live mandi prices)
- `PORT` (provided by most platforms)

Recommended security variables for public deployments:
- `REQUIRE_LOGIN=true`
- `AUTH_MODE=otp` (preferred for farmer-facing deployments)
- `AUTH_USERNAME=<admin username>`
- `AUTH_PASSWORD_HASH=<sha256 password hash>`
- `CHAT_MIN_INTERVAL_SEC=2` (basic per-session throttling)
- `ENABLE_OPERATIONS_DASHBOARD=true` (admin metrics/events page)

OTP mode variables:
- `OTP_WEBHOOK_URL` (SMS gateway/webhook endpoint)
- `OTP_WEBHOOK_BEARER_TOKEN` (optional bearer token)
- `OTP_SENDER_NAME=Trinetra Agro AI`
- `OTP_EXPIRY_SEC=300`
- `OTP_RESEND_INTERVAL_SEC=45`
- `OTP_MAX_ATTEMPTS=5`
- `OTP_ALLOW_DEV_FALLBACK=false` (must remain false in production)

For provider wiring details, see `OTP_WEBHOOK_SETUP.md`.

Example PostgreSQL URL:

```text
postgresql+psycopg2://USER:PASSWORD@HOST:5432/DB_NAME
```

## 2.1) Supabase integration (Step 7 recommended)

Supabase works well for this repo because it provides managed PostgreSQL and backups.

Use the pooled connection string from Supabase (Connection Pooler) and include SSL:

```text
postgresql+psycopg2://postgres.<project-ref>:<password>@aws-0-<region>.pooler.supabase.com:6543/postgres?sslmode=require
```

Setup checklist:
- Create a Supabase project.
- Go to `Project Settings -> Database -> Connection string -> URI`.
- Prefer the **pooler** endpoint for production traffic.
- Set `DATABASE_URL` in your deployment secrets (not in git).
- Run `python healthcheck.py --skip-http` to verify DB connectivity.
- Run `python release_readiness.py --skip-runner --skip-otp-webhook` before go-live.

Notes:
- Current app auto-creates SQLAlchemy tables on startup.
- Keep `sslmode=require` in Supabase connection URL.
- Avoid exposing DB credentials in logs or screenshots.

## 3) Local production-style run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py --server.headless=true --server.address=0.0.0.0 --server.port=8501
```

Windows one-command runner:

```powershell
./start_production.ps1 -CheckOnly
./start_production.ps1 -StartGateway
```

Or directly:

```bash
python production_runner.py --check-only
python production_runner.py --start-gateway
```

Runtime logs:
- `logs/app-production.log`
- `logs/otp-gateway.log`

Runner observability:
- Metrics endpoint: `http://127.0.0.1:9090/metrics`
- Health endpoint: `http://127.0.0.1:9090/healthz`
- Log rotation and retention controlled by:
  - `RUNNER_LOG_MAX_BYTES`
  - `RUNNER_LOG_BACKUP_COUNT`
  - `RUNNER_LOG_RETENTION_DAYS`

Prediction safety:
- `SAFETY_CONFIDENCE_THRESHOLD=0.70`
- When module confidence is below threshold, app shows a caution banner and advises verification with local mandi data / KVK / agri officer.

## 3.1) Release readiness gate (recommended before go-live)

Run one command to validate env, DB, compile checks, production check-only,
runner health/metrics, and OTP webhook (when OTP auth is enabled):

```bash
python release_readiness.py
```

Optional flags:

```bash
python release_readiness.py --skip-runner
python release_readiness.py --skip-otp-webhook
```

## 3.2) Testing pipeline commands

Run unit + integration tests:

```bash
python -m pytest
```

Run smoke verification:

```bash
python quick_start.py
```

Recommended local verification order:

```bash
python -m pytest
python -m compileall app quick_start.py healthcheck.py otp_gateway.py production_runner.py
python release_readiness.py --skip-runner --skip-otp-webhook
```

## 4) Docker deployment

Build image:

```bash
docker build -t trinetra-agro-ai .
```

Run container:

```bash
docker run --rm -p 8501:8501 \
  -e PORT=8501 \
  -e DATABASE_URL="sqlite:///data/trinetra.db" \
  -e OPENROUTER_API_KEY="your_key" \
  trinetra-agro-ai
```

For production, replace SQLite with PostgreSQL in `DATABASE_URL`.

## 4.1) Docker Compose (app + PostgreSQL)

```bash
docker compose up --build
```

This uses `docker-compose.yml` and starts:
- `app` on `http://localhost:8501`
- `db` as PostgreSQL with persistent volume

To stop:

```bash
docker compose down
```

To stop and remove volume data:

```bash
docker compose down -v
```

## 5) Data and persistence notes
- On startup, SQLAlchemy creates tables automatically.
- If you use SQLite in a container, mount a volume for persistence.
- For real users, use PostgreSQL to avoid SQLite concurrency limits.

## 6) Operational checks before go-live
- Start app and verify all sidebar modules load.
- Verify chat in fallback mode (without OpenRouter key) and AI mode (with key).
- Upload at least one image and run disease detection.
- Run one market/risk/yield/profit prediction per crop type.
- Confirm DB inserts by checking table row counts.

## 6.1) Automated health checks

Check DB and Streamlit health endpoint:

```bash
python healthcheck.py
```

Check DB only:

```bash
python healthcheck.py --skip-http
```

Check HTTP only:

```bash
python healthcheck.py --skip-db --health-url http://127.0.0.1:8501/_stcore/health
```

## 7) Safety and reliability recommendations
- Add uptime monitoring and alerting.
- Rotate API keys and keep them in secret managers.
- Back up PostgreSQL daily.
- Keep `REQUIRE_LOGIN=true` for public access unless you add stronger auth.
