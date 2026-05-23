# Trinetra Agro AI — Implementation Plan

## 1. Project Vision
**"Vision Beyond the Fields"** — an investor-ready AI-powered agricultural intelligence SaaS platform. Acts as an AI third eye for farmers, predicting diseases, market prices, risks, irrigation needs, yield, and profitability using ML/DL, predictive analytics, and conversational AI with Telugu voice support.

## 2. Target Architecture

```
Trinetra-Agro-AI/
├── backend/                    # FastAPI server
│   ├── main.py                 # App entry, CORS, lifespan
│   ├── core/                   # Config, security, deps
│   │   ├── config.py
│   │   ├── security.py         # JWT + password hashing
│   │   └── dependencies.py     # DB session, current user
│   ├── auth/                   # Registration, login, tokens
│   │   ├── router.py
│   │   ├── service.py
│   │   └── schemas.py
│   ├── routers/                # Feature route modules
│   │   ├── advisor.py
│   │   ├── disease.py
│   │   ├── market.py
│   │   ├── risk.py
│   │   ├── yield_prediction.py
│   │   ├── irrigation.py
│   │   ├── profit.py
│   │   ├── chatbot.py
│   │   └── feedback.py
│   ├── services/               # Business logic layer
│   ├── schemas/                # Pydantic request/response
│   ├── models/                 # SQLAlchemy ORM models
│   ├── database/               # Engine, session, migrations
│   └── middleware/              # Rate limit, logging
│
├── ai-engine/                  # ML/DL models — decoupled from API
│   ├── disease_detection/
│   │   ├── model.py            # MobileNetV2 transfer learning
│   │   ├── train.py            # Training pipeline
│   │   ├── inference.py        # Grad-CAM, severity, confidence
│   │   └── requirements.txt
│   ├── yield_prediction/
│   │   ├── model.py            # RandomForest + XGBoost ensemble
│   │   ├── train.py
│   │   └── inference.py
│   ├── market_forecasting/
│   │   ├── model.py            # Prophet + optional LSTM
│   │   ├── train.py
│   │   └── inference.py
│   ├── risk_engine/
│   │   ├── model.py            # XGBoost classifier
│   │   ├── train.py
│   │   └── inference.py
│   ├── irrigation_ai/          # Rule-based + weather integration
│   ├── profit_engine/          # Financial calculations
│   ├── recommendation_engine/  # KMeans clustering + similarity
│   └── voice_ai/               # Whisper STT + gTTS TTS
│
├── colab/                       # Google Colab training notebooks
│   ├── disease_detection.ipynb
│   ├── market_forecasting.ipynb
│   ├── risk_engine.ipynb
│   └── yield_prediction.ipynb
│
├── frontend/
│   ├── app.py                  # Streamlit entry + auth
│   ├── pages/                  # One file per feature tab
│   │   ├── 01_dashboard.py
│   │   ├── 02_advisor.py
│   │   ├── 03_disease_scanner.py
│   │   ├── 04_market_intelligence.py
│   │   ├── 05_risk_monitor.py
│   │   ├── 06_yield_prediction.py
│   │   ├── 07_profit_calculator.py
│   │   ├── 08_voice_assistant.py
│   │   └── 09_feedback.py
│   └── components/             # Reusable UI blocks
│       ├── cards.py
│       ├── charts.py
│       ├── sidebar.py
│       └── kpi_widgets.py
│
├── datasets/                   # Sample training data
│   ├── crop_prices.csv
│   ├── yield_data.csv
│   ├── disease_samples/
│   └── weather_samples.csv
│
├── tests/
│   ├── unit/                   # Service/model unit tests
│   ├── integration/            # API integration tests
│   └── e2e/                    # Playwright Streamlit tests
│
├── infra/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── requirements.txt            # Top-level deps (pin versions)
├── .env.example                # All env vars documented
├── README.md                   # Investor-facing + dev guide
└── plan.md                     # This file
```

## 3. Tech Stack Decisions

| Layer | Choice | Why |
|-------|--------|-----|
| Backend | FastAPI | Async, auto-docs (Swagger), Pydantic validation |
| ML/DL | TensorFlow/Keras + Scikit-learn + XGBoost + Prophet | Mature, well-documented, transfer learning ready |
| DB | PostgreSQL + SQLAlchemy + Alembic | Production-grade relational DB with migrations |
| Frontend | Streamlit | Fast iteration, Python-native, data viz built-in |
| Auth | JWT (python-jose) + bcrypt | Stateless, scalable |
| Voice | OpenAI Whisper + gTTS | Offline-capable STT, free TTS |
| Deploy | Docker + Docker Compose | Reproducible, cloud-agnostic |

## 3.5 ML Training Strategy (Google Colab)

Heavy model training is offloaded to **Google Colab** (free Tesla T4 GPU, 15GB VRAM) to avoid:
- Overheating/tying up the development laptop (Intel i5-1235U, integrated GPU, 16GB RAM)
- Hours-long CPU-only training times

| Model | Colab Notebook | Output | Download Back To |
|-------|---------------|--------|------------------|
| MobileNetV2 (Disease) | `colab/disease_detection.ipynb` | `model.h5` | `ai-engine/disease_detection/models/` |
| Prophet (Market) | `colab/market_forecasting.ipynb` | `prophet_model.pkl` | `ai-engine/market_forecasting/models/` |
| XGBoost (Risk) | `colab/risk_engine.ipynb` | `xgb_risk.pkl` | `ai-engine/risk_engine/models/` |
| RF+XGBoost (Yield) | `colab/yield_prediction.ipynb` | `rf_yield.pkl`, `xgb_yield.pkl` | `ai-engine/yield_prediction/models/` |

Workflow: Develop locally → upload notebook to Colab → enable GPU → run training → download `.pkl`/`.h5` → inference locally.

## 4. Database Schema (Key Tables)

| Table | Purpose | Key Columns |
|-------|---------|-------------|
| `users` | Auth & profiles | id, email, hashed_password, created_at |
| `farmers` | Farmer profiles | user_id, soil_type, land_size, location, crops |
| `disease_reports` | Disease detections | farmer_id, image_path, disease, confidence, severity |
| `market_predictions` | Price forecasts | crop, location, forecast_days, predictions_json |
| `risk_assessments` | Risk scores | farmer_id, crop, risk_score, risk_level, factors |
| `yield_predictions` | Yield estimates | farmer_id, crop, fertilizer, rainfall, yield_estimate |
| `irrigation_plans` | Water schedules | farmer_id, crop, daily_litres, schedule_json |
| `profit_analyses` | ROI calculations | farmer_id, crop, revenue, costs, roi_percent |
| `feedback` | User feedback | user_id, feature, rating, comment, timestamp |

## 5. Feature Implementation Details

### 5.1 AI Farming Advisor
- **Inputs**: soil type, land size, budget, irrigation type, crop history
- **Outputs**: recommended crops, fertilizer plan, seasonal calendar, suitability score
- **Approach**: KMeans clustering for farmer segmentation + cosine similarity for crop matching

### 5.2 Disease Detection Engine
- **Model**: MobileNetV2 (transfer learning, pre-trained on ImageNet)
- **Dataset**: PlantVillage (38 classes, 54K images) + custom Indian crop images
- **Outputs**: disease name, confidence %, severity (low/medium/high), Grad-CAM heatmap
- **Training pipeline**: `ai-engine/disease_detection/train.py` → saves `.h5` to disk

### 5.3 Market Price Forecasting
- **Model**: Prophet (primary) + optional LSTM ensemble
- **Forecast horizon**: 7-day and 30-day windows
- **Outputs**: forecast chart, confidence intervals, buy/sell/hold recommendation

### 5.4 Crop Failure Risk Engine
- **Model**: XGBoost classifier
- **Features**: rainfall, temperature, humidity, soil moisture, pest alerts
- **Outputs**: risk score (0-100), risk category (low/medium/high), mitigation steps

### 5.5 Yield Prediction Engine
- **Model**: RandomForest + XGBoost ensemble
- **Features**: fertilizer amount, rainfall, crop type, NPK nutrients, weather
- **Outputs**: expected yield (quintals/acre), optimization suggestions

### 5.6 Smart Irrigation AI
- **Logic**: Rule-based with weather API integration
- **Inputs**: weather forecast, soil moisture, crop type, growth stage
- **Outputs**: watering schedule, water savings estimate vs. traditional

### 5.7 Profit Prediction Engine
- **Logic**: Financial calculation — revenue = yield × predicted_price, costs = seed + fertilizer + labor + irrigation
- **Outputs**: expected revenue, ROI %, break-even point, risk-adjusted profit

### 5.8 Conversational AI Chatbot
- **LLM**: OpenRouter API (free models) with agriculture-specific system prompt
- **Features**: context memory, multilingual (English/Telugu/Hindi), domain guardrails

### 5.9 Voice AI (Telugu-First)
- **STT**: OpenAI Whisper (supports Telugu)
- **TTS**: gTTS with Telugu voice (`te` language code)
- **Flow**: mic input → Whisper → chatbot → gTTS → audio output

### 5.10 Feedback System
- **Collect**: feature used, rating (1-5), comment, timestamp
- **Store**: PostgreSQL `feedback` table
- **Display**: analytics dashboard with average ratings per feature

## 6. Frontend Design System

| Element | Spec |
|---------|------|
| Color primary | `#2E7D32` (Green 800) |
| Color accent | `#66BB6A` (Green 400) |
| Background | `#FAFFFE` (off-white green tint) |
| Font | Inter (Google Fonts) |
| Cards | White, border-radius 14px, box-shadow |
| Charts | Plotly (interactive) |
| Sidebar | Gradient green, navigation selectbox |

**Pages (Streamlit multipage)**:
1. Dashboard — KPI cards, active users, prediction stats, revenue sim
2. AI Advisor — crop recommendations, seasonal plan
3. Disease Scanner — image upload, confidence, treatment
4. Market Intelligence — price charts, forecast, buy/sell advice
5. Risk Monitor — risk gauge, breakdown, mitigations
6. Yield Prediction — estimate, optimization tips
7. Profit Calculator — revenue vs cost chart, ROI, break-even
8. Voice Assistant — mic button, Telugu output
9. Feedback — star rating, comment form

## 7. Development Phases (Priority Order)

### Phase 1 — Foundation (Backend + Auth + DB + UI Skeleton)
- FastAPI project setup with CORS, lifespan
- PostgreSQL + SQLAlchemy models + Alembic migrations
- JWT auth (register, login, token refresh)
- Streamlit multipage shell with all pages stubbed

### Phase 2 — Core AI Features
- AI Farming Advisor with recommendation engine
- Yield Prediction with RF+XGBoost ensemble
- Profit Prediction engine

### Phase 3 — Advanced AI Features
- Disease Detection (MobileNetV2, training pipeline, Grad-CAM)
- Risk Engine (XGBoost)
- Market Forecasting (Prophet)

### Phase 4 — Conversational & Voice AI
- Chatbot with OpenRouter, system prompt, context memory
- Voice AI (Whisper + gTTS Telugu)

### Phase 5 — Production Hardening
- Analytics dashboard
- Feedback system
- Docker + docker-compose
- Full test suite (unit, integration, E2E)
- Deployment documentation (Render, Railway, AWS, DigitalOcean)

## 8. Testing Strategy

| Type | Tool | Coverage Target |
|------|------|-----------------|
| Unit tests | pytest | Services, models, utilities |
| API tests | pytest + httpx | All endpoints, auth flows |
| Model tests | pytest | Inference output shape, confidence range |
| Integration | pytest | DB writes, end-to-end prediction flow |
| E2E | Playwright | Streamlit UI flows, all feature tabs |

## 9. Deployment Targets

| Platform | Notes |
|----------|-------|
| **Render** | Easiest — native Python + Docker support, free tier available |
| **Railway** | Similar to Render, good free tier |
| **Hugging Face Spaces** | Free Streamlit hosting (no backend needed for demo) |
| **AWS EC2 + RDS** | Full control, production scale |
| **DigitalOcean App Platform** | Managed Docker, PostgreSQL included |

Deployment artifacts: `Dockerfile`, `docker-compose.yml`, `nginx.conf`, `.env.example`

## 10. Success Criteria

- All 10 core features functional end-to-end
- Clean separation: API routes → services → AI engine
- Authentication working with JWT
- PostgreSQL with all tables and Alembic migrations
- Docker one-command startup (`docker compose up`)
- Investor-demo ready: polished UI, real predictions, professional README
- All tests passing
