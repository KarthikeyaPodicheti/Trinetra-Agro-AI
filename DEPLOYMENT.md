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
- `PORT` (provided by most platforms)

Recommended security variables for public deployments:
- `REQUIRE_LOGIN=true`
- `AUTH_USERNAME=<admin username>`
- `AUTH_PASSWORD_HASH=<sha256 password hash>`
- `CHAT_MIN_INTERVAL_SEC=2` (basic per-session throttling)
- `ENABLE_OPERATIONS_DASHBOARD=true` (admin metrics/events page)

Example PostgreSQL URL:

```text
postgresql+psycopg2://USER:PASSWORD@HOST:5432/DB_NAME
```

## 3) Local production-style run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app/main.py --server.headless=true --server.address=0.0.0.0 --server.port=8501
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
