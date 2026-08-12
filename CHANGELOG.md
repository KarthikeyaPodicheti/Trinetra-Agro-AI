# Changelog

All notable changes to Trinetra Agro AI are documented here. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.0.0] — 2026-08-12

### Added

- **Backend test suite** (`backend/tests/`) — 56 hermetic tests covering:
  - Auth API: register, login, `/auth/me`, token refresh, OTP endpoints (runs
    against SQLite, no network, no real credentials)
  - `core/security.py`: bcrypt hashing + JWT creation/validation/expiry
  - `auth/otp_service.py`: phone normalization, OTP store/verify, SMS gateway
    console fallback
  - `services/mandi_service.py`: record parsing, trend analysis, buy/sell/hold
    recommendations, 30-minute cache (network fully mocked)
  - System/health/root and the AI market endpoint (synthetic fallback)
- `backend/requirements-dev.txt` — pytest + pytest-asyncio + aiosqlite + httpx
- CI now runs the test suite on every push/PR in addition to the compile check

### Fixed

- **`/auth/send-otp` returned HTTP 500** — `Settings.fast2sms_api_key` was
  referenced by the OTP router and config `__init__` but never declared as a
  field. Declared it on `Settings` (`backend/core/config.py`).
- **`loguru` missing from `requirements.txt`** — imported at module load by the
  logging middleware; a fresh install could not import the app.
- **`numpy` missing from `requirements.txt`** — imported at module load by
  `ai_engine/disease_detection/inference.py`.

---

## Project history (pre-1.0.0)

Prior to 1.0.0 the project shipped without releases. Notable historical fixes
are documented in the "Deployment Journey" postmortem section of the README
(features, deployment bugs #1–#8, and troubleshooting).