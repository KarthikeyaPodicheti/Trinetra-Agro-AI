# Trinetra Agro AI — Implementation Plan

## Phase 1: Foundation — Backend + Database + Auth *(~4 days)*

### Step 1.1 — Project Scaffold
- Create `backend/` directory with `main.py`, `core/`, `routers/`, `services/`, `schemas/`, `models/`, `middleware/`
- Create `frontend/` with `app.py`, `pages/`, `components/`
- Create `ai-engine/` with subdirectories for each ML module
- Write `requirements.txt` with all pinned versions (fastapi, uvicorn, sqlalchemy, alembic, passlib, python-jose, tensorflow, xgboost, prophet, openai-whisper, etc.)
- Move existing `data/`, `tests/`, `infra/` into new structure

### Step 1.2 — Database Models
- Write all 9 SQLAlchemy models in `backend/models/`
- Set up Alembic with `alembic init`, configure `env.py` for async PostgreSQL
- Generate initial migration, test `alembic upgrade head`

### Step 1.3 — Auth System
- Write `User` model with bcrypt password hashing
- Implement `/auth/register`, `/auth/login`, `/auth/refresh` endpoints in `backend/auth/`
- Write JWT creation/validation in `backend/core/security.py`
- Add `get_current_user` dependency in `backend/core/dependencies.py`
- Write Pydantic schemas: `UserCreate`, `UserLogin`, `TokenResponse`

### Step 1.4 — FastAPI Core
- `backend/main.py` — app factory with CORS, lifespan, router registration
- `backend/core/config.py` — Settings class with all env vars
- `backend/middleware/logging.py` — request/response logging
- `backend/middleware/rate_limit.py` — simple in-memory rate limiter
- Health check endpoint

---

## Phase 2: AI Engine — Replace Heuristics with ML *(~5 days)*

**Training strategy**: All models train locally on CPU (Intel i5-1235U, 16GB RAM). MobileNetV2 uses transfer learning — feature extraction only (freeze base, train classification head, ~10-15 min). XGBoost, RF, Prophet, KMeans are CPU-native (~2-10 seconds each). Trained models saved to `ai-engine/*/models/`.

### Step 2.1 — Disease Detection (MobileNetV2)
- Write `ai-engine/disease_detection/train.py` — download PlantVillage, MobileNetV2 feature extraction (freeze base, train head), save `.h5` (~10-15 min CPU)
- Write `ai-engine/disease_detection/inference.py` — load model, predict, Grad-CAM heatmap, confidence + severity
- Write `backend/routers/disease.py` + `backend/services/disease_service.py`
- Frontend: `frontend/pages/03_disease_scanner.py`

### Step 2.2 — Market Forecasting (Prophet)
- Write `ai-engine/market_forecasting/train.py` — generate synthetic crop price data, train Prophet, save `.pkl` (~10 sec CPU)
- Write `ai-engine/market_forecasting/inference.py` — 7-day and 30-day forecast with confidence intervals
- Write `backend/routers/market.py` + `backend/services/market_service.py`
- Frontend: `frontend/pages/04_market_intelligence.py`

### Step 2.3 — Risk Engine (XGBoost)
- Write `ai-engine/risk_engine/train.py` — generate synthetic weather/soil/pest data, train XGBoost, save `.pkl` (~5 sec CPU)
- Write `ai-engine/risk_engine/inference.py` — risk score, category, feature importance
- Write `backend/routers/risk.py` + `backend/services/risk_service.py`
- Frontend: `frontend/pages/05_risk_monitor.py`

### Step 2.4 — Yield Prediction (RF + XGBoost)
- Write `ai-engine/yield_prediction/train.py` — generate synthetic yield data, train RF+XGBoost ensemble, save `.pkl` (~5 sec CPU)
- Write `ai-engine/yield_prediction/inference.py`
- Write `backend/routers/yield_prediction.py` + service
- Frontend: `frontend/pages/06_yield_prediction.py`

### Step 2.5 — Crop Advisor (KMeans + Similarity)
- Write `ai-engine/recommendation_engine/model.py` — KMeans clustering + cosine similarity
- Write `backend/routers/advisor.py` + service
- Frontend: `frontend/pages/02_advisor.py`

### Step 2.6 — Irrigation + Profit (Rule-based, Refactored)
- Move existing `irrigation_ai.py` and `profit_predictor.py` into `ai-engine/`
- Write `backend/routers/irrigation.py` + `backend/routers/profit.py` + services
- Frontend: `frontend/pages/07_profit_calculator.py`

---

## Phase 3: Chatbot + Voice AI *(~3 days)*

### Step 3.1 — Chatbot (Port + Enhance)
- Port existing `chatbot/core_bot.py` into `backend/services/chatbot_service.py`
- Update to use OpenRouter client from backend config
- Write `backend/routers/chatbot.py` with streaming support
- Frontend: integrate into dashboard sidebar as persistent chat

### Step 3.2 — Voice AI (Whisper + gTTS)
- Write `ai-engine/voice_ai/stt.py` — Whisper speech-to-text (Telugu, Hindi, English)
- Write `ai-engine/voice_ai/tts.py` — gTTS text-to-speech
- Write `backend/routers/voice.py` + service
- Frontend: `frontend/pages/08_voice_assistant.py` with mic upload + audio playback

---

## Phase 4: Frontend — SaaS Dashboard *(~3 days)*

### Step 4.1 — Multipage Shell
- `frontend/app.py` — entry point with auth check, sidebar nav, session state
- `frontend/components/sidebar.py` — reusable sidebar with farmer profile + navigation
- `frontend/components/cards.py` — stat card, feature card components
- `frontend/components/charts.py` — Plotly chart wrappers
- `frontend/components/kpi_widgets.py` — metric tiles

### Step 4.2 — Dashboard Page
- `frontend/pages/01_dashboard.py` — KPI overview: active users, predictions run, avg ROI, disease detections, risk trends
- Connect to backend analytics endpoints

### Step 4.3 — Feedback Page
- `frontend/pages/09_feedback.py` — star rating, comment form per feature
- Write `backend/routers/feedback.py` + `backend/services/feedback_service.py`
- `Feedback` SQLAlchemy model + Alembic migration

---

## Phase 5: Testing *(~2 days)*

### Step 5.1 — Unit Tests
- `tests/unit/test_security.py` — JWT encode/decode, password hashing
- `tests/unit/test_models.py` — SQLAlchemy model creation/validation
- `tests/unit/test_services.py` — each service layer function

### Step 5.2 — API Integration Tests
- `tests/integration/test_auth.py` — register to login to token to protected endpoint
- `tests/integration/test_disease.py` — upload image to get prediction
- `tests/integration/test_market.py` — predict to verify response schema
- All 9 feature routers tested via `httpx` + `TestClient`

### Step 5.3 — Model Inference Tests
- `tests/unit/test_disease_model.py` — output shape, confidence 0-1 range, Grad-CAM array
- `tests/unit/test_market_model.py` — forecast length, confidence intervals
- `tests/unit/test_risk_model.py` — probability 0-1, category mapping

### Step 5.4 — E2E Playwright Tests
- Full flow: login to navigate each tab to run predictions to verify UI elements
- Chatbot send message to verify AI response
- Voice assistant upload to verify response

---

## Phase 6: Production Hardening *(~2 days)*

### Step 6.1 — Docker + Compose
- Update `Dockerfile` — multi-stage build (backend + frontend), optimized layers
- Update `docker-compose.yml` — app + PostgreSQL + optional Redis
- Add `.dockerignore`

### Step 6.2 — Nginx + SSL
- Write `infra/nginx.conf` — reverse proxy to FastAPI + Streamlit, SSL template

### Step 6.3 — CI/CD
- `.github/workflows/ci.yml` — lint, typecheck, test, build Docker image
- `.github/workflows/deploy.yml` — deploy to Render/Railway on push to main

### Step 6.4 — README + Docs
- Complete README: architecture diagram, setup, API docs link, deploy guide, screenshots
- `DEPLOYMENT.md` — platform-specific guides (Render, Railway, AWS, DO)

---

## Total Time Estimate

| Phase | Description | Effort | Training |
|-------|-------------|--------|----------|
| 1 | Foundation (FastAPI, DB, Auth) | ~4 days | — |
| 2 | AI Engine (6 ML models) | ~5 days | Colab GPU |
| 3 | Chatbot + Voice AI | ~3 days | — |
| 4 | Frontend (SaaS dashboard) | ~3 days | — |
| 5 | Testing (unit + integration + E2E) | ~2 days | — |
| 6 | Production hardening (Docker, CI/CD, docs) | ~2 days | — |
| **Total** | | **~19 days** | |

**Note**: All Phase 2 models train directly on local CPU. MobileNetV2 uses transfer learning (feature extraction only, freezes pre-trained base, trains classification head — ~10-15 min). XGBoost, RF, Prophet are CPU-native (~2-10 sec each).
