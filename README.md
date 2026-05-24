# 🔱 Trinetra Agro AI — Vision Beyond the Fields

An AI-powered agricultural intelligence platform for Indian farmers with multilingual support (English, Hindi, Telugu).

![Next.js](https://img.shields.io/badge/Next.js-16-black) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green) ![Supabase](https://img.shields.io/badge/Database-Supabase-darkgreen) ![LLM](https://img.shields.io/badge/LLM-Gemma_4-blue)

---

## 🌾 Features

| Feature | Description |
|---------|-------------|
| **AI Chatbot** | Conversational farming assistant powered by Gemma LLM (OpenRouter). Responds in English, Hindi, or Telugu. |
| **Disease Scanner** | Upload a leaf image → MobileNetV2 model identifies disease, severity, treatment, and prevention tips. |
| **Market Intelligence** | Real mandi prices from data.gov.in API with trend analysis and buy/sell/hold recommendations. |
| **Weather Advisory** | Live weather from Open-Meteo (free) with farming-specific advice based on temperature. |
| **Seasonal Dashboard** | Shows current season crops, tasks checklist, and actionable farming tips. |
| **Multilingual UI** | Full app available in English, हिन्दी, and తెలుగు — toggle from sidebar. |
| **OTP Login** | Phone-based OTP authentication via Fast2SMS alongside email/password login. |

---

## 🖼️ Preview

### Login Page (Liquid Glass Effect)
![Login Page](screenshots/login.png)

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Next.js 16     │────▶│  FastAPI Backend  │────▶│  Supabase       │
│  (Port 3000)    │     │  (Port 8000)      │     │  PostgreSQL     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                    ┌─────────┼─────────┐
                    ▼         ▼         ▼
              OpenRouter   data.gov.in  Fast2SMS
              (Gemma LLM)  (Mandi API)  (OTP)
```

---

## 📁 Project Structure

```
Trinetra-Agro-AI/
├── backend/                    # FastAPI Python backend
│   ├── main.py                 # App entry point
│   ├── requirements.txt        # Python dependencies
│   ├── auth/                   # Authentication (JWT + OTP)
│   │   ├── router.py           # /auth endpoints
│   │   ├── service.py          # User creation, password hashing
│   │   └── otp_service.py      # OTP generation + Fast2SMS
│   ├── routers/                # API route handlers
│   │   ├── ai_features.py      # /ai/market
│   │   ├── chatbot.py          # /chat/send, /chat/clear
│   │   ├── disease.py          # /ai/disease (image upload)
│   │   └── feedback.py         # /feedback
│   ├── services/               # Business logic
│   │   ├── ai_service.py       # Market forecast orchestration
│   │   ├── chatbot_service.py  # Chat session management
│   │   ├── openrouter_service.py # LLM API client
│   │   └── disease_service.py  # Disease inference wrapper
│   ├── schemas/                # Pydantic request/response models
│   ├── models/                 # SQLAlchemy ORM models (9 tables)
│   ├── database/               # Async DB session (Supabase)
│   ├── core/                   # Config, JWT security, dependencies
│   └── middleware/             # Request logging
├── frontend-next/              # Next.js frontend
│   ├── src/app/                # App Router pages
│   │   ├── page.tsx            # Dashboard
│   │   ├── login/              # Login (liquid glass effect)
│   │   ├── register/           # Registration
│   │   ├── chatbot/            # AI Chatbot
│   │   ├── disease-scanner/    # Disease detection
│   │   ├── market/             # Market intelligence
│   │   ├── feedback/           # Feedback form
│   │   ├── app-shell.tsx       # Sidebar + layout
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Glassmorphism styles
│   ├── src/lib/                # Utilities
│   │   ├── api.ts              # API client with auto-refresh
│   │   ├── auth.ts             # Auth functions
│   │   ├── language.tsx        # i18n context (EN/HI/TE)
│   │   └── types.ts            # TypeScript interfaces
│   ├── src/components/         # Shared components
│   ├── middleware.ts           # Auth route guard
│   └── public/bg.jpg           # Background image
├── ai_engine/                  # AI/ML modules
│   ├── market_forecasting/     # Real mandi data + trend analysis
│   └── disease_detection/      # MobileNetV2 inference + training
├── supabase/                   # Database
│   ├── migrations/             # SQL schema migrations
│   └── config.toml             # Supabase project config
├── .env                        # Environment variables
└── .github/workflows/ci.yml    # GitHub Actions CI
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- Supabase account (free tier works)
- OpenRouter API key (free models available)

### 1. Clone & Install

```bash
git clone https://github.com/KarthikeyaPodicheti/Trinetra-Agro-AI.git
cd Trinetra-Agro-AI

# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend-next
npm install
```

### 2. Configure Environment

Create `.env` in the project root:

```env
# Database (Supabase)
DATABASE_URL=postgresql+asyncpg://postgres.[ref]:[password]@aws-0-[region].pooler.supabase.com:6543/postgres

# Auth
SECRET_KEY=your-secret-key-here

# LLM (OpenRouter - get free key at openrouter.ai)
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=google/gemma-4-26b-a4b-it:free

# Market Data (register at data.gov.in)
DATA_GOV_API_KEY=your-key-here

# Supabase
SUPABASE_URL=https://[ref].supabase.co
SUPABASE_PROJECT_REF=[ref]
```

Create `frontend-next/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Setup Database

Push migrations to Supabase:
```bash
npx supabase db push
```

### 4. Run

```bash
# Terminal 1 — Backend
cd Trinetra-Agro-AI
python -m uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend-next
npm run dev
```

Open http://localhost:3000

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Email/password login → JWT |
| POST | `/auth/send-otp` | Send OTP to phone |
| POST | `/auth/verify-otp` | Verify OTP → JWT |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Get current user |
| POST | `/ai/market` | Market price forecast |
| POST | `/ai/disease` | Disease detection (multipart image) |
| POST | `/chat/send` | Send chat message |
| POST | `/chat/clear` | Clear chat session |
| POST | `/feedback` | Submit feedback |
| GET | `/health` | Health check |

---

## 🌐 External Services

| Service | Purpose | Cost |
|---------|---------|------|
| [OpenRouter](https://openrouter.ai) | LLM for chatbot & translations | Free (Gemma model) |
| [data.gov.in](https://data.gov.in) | Real mandi crop prices | Free (API key required) |
| [Open-Meteo](https://open-meteo.com) | Weather data | Free (no key needed) |
| [Fast2SMS](https://fast2sms.com) | OTP delivery | Paid (₹ per SMS) |
| [Supabase](https://supabase.com) | PostgreSQL database | Free tier available |

---

## 🗄️ Database Schema

| Table | Purpose |
|-------|---------|
| `users` | User accounts (email, password, phone) |
| `farmers` | Farmer profiles (soil, land, location, crops) |
| `disease_reports` | Disease scan history |
| `market_predictions` | Market forecast history |
| `feedback` | User feedback submissions |

---

## 🌍 Multilingual Support

The app supports 3 languages, switchable from the sidebar:

- **English** — Default
- **हिन्दी (Hindi)** — Full UI + chatbot responds in Hindi
- **తెలుగు (Telugu)** — Full UI + chatbot responds in Telugu

The language context (`src/lib/language.tsx`) provides translations for all UI strings. The chatbot's language is passed to the LLM so responses come back in the selected language.

---

## 🧠 AI/ML

### Disease Detection
- **Model**: MobileNetV2 (transfer learning)
- **Dataset**: PlantVillage (38 classes, 70K+ images)
- **Training**: Google Colab with GPU
- **Inference**: Upload leaf image → disease name, confidence, severity, treatment

### Market Forecasting
- **Data Source**: data.gov.in real mandi prices
- **Analysis**: Trend detection from recent vs historical records
- **Fallback**: Synthetic estimates when API unavailable

---

## 🎨 UI Design

- **Glassmorphism** — Frosted glass cards with `backdrop-filter: blur`
- **Liquid Glass** — SVG filter distortion on login/register pages
- **Green gradient** background across dashboard
- **Responsive** — Mobile sidebar overlay, desktop fixed sidebar

---

## 📄 License

MIT

---

## 👨‍💻 Author

**Karthikeya Podicheti**
- GitHub: [@KarthikeyaPodicheti](https://github.com/KarthikeyaPodicheti)
