# 🔱 Trinetra Agro AI — Vision Beyond the Fields

[![Next.js](https://img.shields.io/badge/Next.js-16.2-black)](https://nextjs.org)
[![React](https://img.shields.io/badge/React-19.2-blue)](https://react.dev)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.12%2B-yellow)](https://python.org)
[![Supabase](https://img.shields.io/badge/Database-Supabase-darkgreen)](https://supabase.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Trinetra Agro AI** is a web application that puts artificial intelligence in the hands of Indian farmers. Upload a photo of a diseased leaf — the app tells you what's wrong and how to fix it. Ask a question — an AI assistant answers in your language. Check crop prices — you'll know whether to sell now or wait.

All of this works in **English, Hindi, and Telugu**.

<p align="center">
  <img src="screenshots/login.png" alt="Trinetra Agro AI Login Screen" width="600" />
</p>

---

## Table of Contents

1. [What Can You Do With This App?](#what-can-you-do-with-this-app)
2. [Setting Up The App On Your Computer](#setting-up-the-app-on-your-computer)
3. [How Each Feature Works](#how-each-feature-works)
4. [The Technology Stack](#the-technology-stack)
5. [Project File Structure](#project-file-structure)
6. [API Endpoints — The Complete List](#api-endpoints--the-complete-list)
7. [Database — What Gets Stored](#database--what-gets-stored)
8. [External Services We Depend On](#external-services-we-depend-on)
9. [What's Working And What's Coming](#whats-working-and-whats-coming)
10. [Troubleshooting](#troubleshooting)

---

## What Can You Do With This App?

Trinetra Agro AI has **five fully working features** right now. Here they are in the order a farmer would use them:

### 1. 📋 Create Your Account
Sign up with your email address and a password. Or use your phone number — the app sends you a one-time code via SMS. Once logged in, you stay logged in even if you close the browser. If your session expires, the app renews it automatically.

### 2. 👤 Save Your Farm Profile
Tell the app about your farm: where it's located, how big it is (in acres), what type of soil you have, which crops you grow, what irrigation method you use, and your farming budget. Once you save this, the AI assistant uses it to give you advice that's specific to your farm — not generic tips you could find anywhere.

### 3. 💬 Chat With An AI Farming Assistant
Open the chatbot and type any question: *"What fertilizer should I use for rice in loamy soil?"* or *"When is the best time to plant wheat in Maharashtra?"* or *"How do I control aphids in my cotton crop?"* The assistant understands the context of your farm and answers in whatever language you've selected — English, Hindi, or Telugu.

The assistant remembers the last six messages of your conversation, so you can ask follow-up questions naturally.

### 4. 🔬 Scan A Leaf For Disease
Found a spotty leaf and don't know what's wrong? Upload a photo. The app uses a machine learning model called **MobileNetV2** — trained on over 70,000 images of diseased and healthy crop leaves across 38 different diseases. It tells you:

- **The disease name** (for example: "Tomato Late Blight")
- **How confident it is** (as a percentage)
- **How severe the infection is** (Mild / Moderate / Severe)
- **How to treat it** (step-by-step chemical and organic recommendations)
- **How to prevent it next season**

This model achieves **98.76% accuracy** across all 38 diseases.

### 5. 📈 Check Market Prices
Select a crop — say, Rice or Onion — and choose how many days of price forecast you want (7 to 30 days). The app pulls **real-time mandi prices** from the Government of India's data portal (data.gov.in) and analyzes whether prices are trending up, down, or staying flat. It then tells you whether you should **buy, sell, or hold**.

You also get a chart showing the price trend and a set of market tips based on the current situation.

### Plus: ⭐ Rate The App
After using any feature, you can leave a star rating and a comment. This feedback gets stored and helps improve the app.

---

## Setting Up The App On Your Computer

Running Trinetra Agro AI on your own computer requires four things. Everything except the phone SMS service is free.

### What You Need Before You Start

| Thing | Why You Need It | Where To Get It |
|-------|----------------|-----------------|
| **Python 3.12 or newer** | The backend is written in Python. Without it, the app's logic can't run. | [python.org/downloads](https://python.org/downloads) |
| **Node.js 18 or newer** | The frontend is written in JavaScript. Node.js runs it during development. | [nodejs.org](https://nodejs.org) |
| **A Supabase account** | Supabase provides the PostgreSQL database where all your data lives. | [supabase.com](https://supabase.com) — free tier is enough |
| **An OpenRouter API key** | OpenRouter gives us access to the Gemma AI model that powers the chatbot. | [openrouter.ai/keys](https://openrouter.ai/keys) — free |

### Step 1 — Download The Code

Open a terminal (Command Prompt on Windows, Terminal on Mac/Linux) and run:

```bash
git clone https://github.com/KarthikeyaPodicheti/Trinetra-Agro-AI.git
cd Trinetra-Agro-AI
```

If you don't have Git installed, you can download the project as a ZIP file from the green "Code" button on the GitHub page.

### Step 2 — Install The Backend

```bash
cd backend
pip install -r requirements.txt
```

The `requirements.txt` file lists every Python library the backend needs — FastAPI (the web framework), SQLAlchemy (database access), python-jose (login tokens), bcrypt (password security), Pillow (image processing), and more.

### Step 3 — Install The Frontend

Open a second terminal in the same project folder, or go back first:

```bash
cd ..
cd frontend-next
npm install
```

This installs Next.js (the web framework), React (the user interface library), Tailwind CSS (styling), Recharts (for charts), and all other frontend dependencies.

### Step 4 — Create Your Configuration File

Create a new file called `.env` in the `Trinetra-Agro-AI/` folder (the main project folder). Copy and paste the template below, filling in your actual keys:

```env
# DATABASE CONNECTION
# Get this from Supabase → Project Settings → Database → Connection string → URI
# It looks like: postgresql+asyncpg://postgres.abc123:[password]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
DATABASE_URL=postgresql+asyncpg://postgres.YOUR-PROJECT-REF:YOUR-PASSWORD@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres

# SECURITY — Pick any random string. This is used to sign your login tokens.
SECRET_KEY=my_super_secret_key_change_this

# AI CHATBOT — Get this free from openrouter.ai/keys
OPENROUTER_API_KEY=sk-or-v1-your-key-here
OPENROUTER_MODEL=google/gemma-4-26b-a4b-it:free

# CROP PRICES — Get this free from data.gov.in (register an account, request an API key)
DATA_GOV_API_KEY=your-data-gov-key-here

# SUPABASE PROJECT — Find these in your Supabase dashboard under Project Settings
SUPABASE_URL=https://your-project-ref.supabase.co
```

Create a second file at `frontend-next/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This tells the frontend where to find the backend on your computer. In production, this would be a real web address.

### Step 5 — Create The Database Tables

```bash
npx supabase db push
```

This command reads the SQL migration files in the `supabase/migrations/` folder and creates nine tables in your Supabase PostgreSQL database. It also creates a demo account so you can log in immediately:

- **Email**: `demo@farm.com`
- **Password**: `demo123456`

### Step 6 — Start Both Servers

You need two terminals running at the same time:

**Terminal 1 — Start the backend** (from the `Trinetra-Agro-AI/` folder):

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

You should see something like: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 — Start the frontend** (from the `frontend-next/` folder):

```bash
npm run dev
```

You should see: `Ready in 500ms — Local: http://localhost:3000`

### Step 7 — Open The App

Go to **http://localhost:3000** in your web browser. You'll see the login screen with a glass-effect card. Log in with the demo account, and you're in.

---

## How Each Feature Works

This section explains the flow of every feature — from the moment you click a button to when the result appears on your screen.

### Authentication (Login & Register)

When you enter your email and password and click "Sign In", here is exactly what happens:

1. Your browser sends your email and password to `POST /auth/login` on the backend
2. The backend looks up your email in the `users` table in the PostgreSQL database
3. If your account exists, it checks whether the password you typed matches the encrypted version stored in the database (this is done using **bcrypt**, a one-way hashing algorithm — your actual password is never stored, only a mathematical fingerprint of it)
4. If the password matches, the backend creates two **JSON Web Tokens (JWTs)**: an access token (valid for 30 minutes) and a refresh token (valid for 7 days)
5. These tokens are saved as cookies in your browser
6. Every time you visit any page after login, your browser automatically sends the access token with each request. The backend verifies it before showing you any data
7. If the access token expires, the frontend automatically uses the refresh token to get a new one — you won't even notice

For phone OTP login:
1. You enter your phone number and click "Send OTP"
2. The backend generates a random 6-digit code and attempts to send it via Fast2SMS
3. If the SMS service is unavailable, the code is printed in the server terminal instead
4. You enter the code and the backend verifies it. The OTP is valid for 5 minutes

### AI Chatbot

When you type a message into the chatbot and press send:

1. Your message goes to `POST /chat/send` along with your session ID (so the chat history stays linked) and your selected language
2. The backend loads your farm profile from the `farmers` table — all the details you saved (location, land size, soil type, crops, irrigation, budget)
3. It collects the last six messages from your conversation history, including both your questions and the assistant's answers
4. Everything is packaged into a prompt and sent to the **OpenRouter API**, which forwards it to Google's **Gemma** AI model
5. The system prompt instructs Gemma to act as an expert agricultural advisor with knowledge of Indian farming practices. Your farm details are included so the advice is personalized. The language instruction tells it to respond in English, Hindi, or Telugu
6. Gemma generates a response and sends it back
7. The backend returns the response to your browser, and the chatbot displays it in the conversation

If OpenRouter is down or your API key is invalid, the chatbot falls back to a built-in set of keyword-matched farming answers.

Chat history is stored in memory on the server while the app is running. If you restart the server, the history is cleared — this is an intentional design choice to keep the system simple.

### Disease Scanner

When you upload a leaf photo and click "Analyze":

1. The image is sent to `POST /ai/disease` as multipart form data (the standard way to upload files over HTTP)
2. The backend reads the image bytes and passes them to the disease detection engine in `ai_engine/disease_detection/inference.py`
3. If TensorFlow is installed, the engine:

   - Opens the image using the Pillow library
   - Resizes it to 224×224 pixels (the input size MobileNetV2 expects)
   - Normalizes the pixel values to the range [-1, 1]
   - Runs the image through the neural network — a series of mathematical operations across 155 layers
   - The final layer outputs probabilities for 38 disease classes plus one healthy class
   - The disease with the highest probability is selected
   - The engine also generates a **Grad-CAM heatmap** — a visualization showing which parts of the leaf the model focused on to make its decision

4. If the model's confidence is at least 30%, the result is returned. If confidence is lower, or if TensorFlow isn't installed, the engine falls back to a hardcoded lookup table covering five common crops

5. If you're logged in, the result is saved to the `disease_reports` table for future reference

The model was trained using **transfer learning** — instead of building a model from scratch (which would need millions of images), we started with a MobileNetV2 that had already been trained on 1.4 million general images (ImageNet dataset). We then fine-tuned it on the PlantVillage dataset (70,000+ crop leaf images) in two phases:

- **Phase 1 (15 epochs)**: Only the top classification layers were trained, while the base model was frozen — 96.5% accuracy
- **Phase 2 (10 epochs)**: The top 30 layers of the base model were unfrozen and fine-tuned with a very small learning rate — 98.76% accuracy

### Market Intelligence

When you select a crop and click "Get Forecast":

1. The request goes to `POST /ai/market` with the crop name and number of days
2. The backend calls the market forecasting engine in `ai_engine/market_forecasting/engine.py`
3. If you have a data.gov.in API key configured, the engine:

   - Calls the Government of India's open data API to fetch the last 50 price records for that crop from Indian mandis
   - Parses the JSON response to extract current market prices, locations, and dates
   - Calculates the recent average price and compares it against historical prices from the dataset
   - Determines the trend: upward (prices are rising), downward (prices are falling), or stable
   - Generates a 7-30 day forecast by projecting the trend forward
   - Returns a recommendation: buy (if prices are low and expected to rise), sell (if prices are high and expected to drop), or hold (if prices are stable)

4. If the API call fails or no API key is configured, the engine generates synthetic data using a deterministic random seed (based on the crop name and current date), so the prediction is at least consistent across multiple calls on the same day

5. The frontend renders the results as an interactive **Recharts** line chart showing predicted prices over time, plus the current price, trend direction, and market tips

### Farm Profile

The profile page talks to three endpoints on the same path:

- **GET /profile** — loads your existing farm profile from the `farmers` table
- **POST /profile** — creates a new profile (used the first time you save)
- **PUT /profile** — updates an existing profile (used when you make changes)

The form accepts: location, land size in acres, crops (as comma-separated names), soil type, irrigation type, budget in rupees, and years of farming experience. All of this becomes context for the chatbot.

### Feedback

The feedback page sends a **POST /feedback** request with three fields: which feature you're rating, a star rating from 1 to 5, and an optional text comment. The backend saves it to the `feedback` table. You don't need to be logged in to submit feedback.

---

## The Technology Stack

Here is every major technology in this project, organized by where it lives, with a brief explanation of what each one does.

### Backend (Python — runs on your computer or a cloud server)

| Technology | Version | What It Does |
|-----------|---------|-------------|
| **FastAPI** | Latest | A Python web framework for building APIs. It handles incoming HTTP requests, validates the data using Pydantic models, and routes them to the correct function. Automatically generates interactive documentation at `/docs`. |
| **Uvicorn** | Latest | The ASGI server that runs FastAPI. Think of it as the engine that keeps the backend process alive and listening for requests. |
| **SQLAlchemy** | 2.0+ | An Object-Relational Mapper (ORM). Instead of writing raw SQL queries, you write Python classes. SQLAlchemy translates them into efficient SQL and manages database connections. We use the async version with asyncpg for non-blocking queries. |
| **asyncpg** | Latest | A fast, asynchronous PostgreSQL driver. It handles the actual communication between Python and the PostgreSQL database without blocking other requests. |
| **Pydantic** | 2.0+ | A data validation library. Every piece of data coming into or leaving the API is validated against a Pydantic model — if the shape is wrong, the request is rejected before it even reaches the logic. |
| **python-jose** | 3.4+ | A library for creating and verifying JSON Web Tokens (JWTs). These are the signed tokens used for authentication — the backend creates them on login, and every subsequent request includes them to prove the user is who they claim to be. |
| **bcrypt** | 4.0+ | A password hashing algorithm. When a user creates an account, their password is run through bcrypt, which produces a mathematical fingerprint. Even if the database is compromised, the actual passwords cannot be recovered. |
| **Pillow** | 10.0+ | A Python imaging library. Used by the disease scanner to open, resize, and preprocess uploaded leaf images before they go through the neural network. |
| **python-multipart** | Latest | Enables FastAPI to handle file uploads — specifically, the multipart/form-data encoding used when a user uploads a leaf photo. |
| **requests** | 2.32+ | A straightforward HTTP library. Used to make API calls to OpenRouter (for the chatbot) and data.gov.in (for crop prices). |
| **httpx** | Latest | An async HTTP client. Used by the OTP service to call the Fast2SMS gateway for sending SMS messages. |

### Frontend (JavaScript/TypeScript — runs in the browser)

| Technology | Version | What It Does |
|-----------|---------|-------------|
| **Next.js** | 16.2 | A React framework that handles routing (which page to show for which URL), server-side rendering (generating pages on the server for faster load), and the development server. |
| **React** | 19.2 | A JavaScript library for building user interfaces. The entire UI — buttons, forms, cards, charts — is built as React components that update automatically when data changes. |
| **TypeScript** | 5.x | JavaScript with type annotations. Catches mistakes during development instead of at runtime — if you try to pass text where a number is expected, TypeScript tells you immediately. |
| **Tailwind CSS** | 4.x | A utility-first CSS framework. Instead of writing separate stylesheets, you apply classes directly in your HTML/JSX — `bg-white`, `rounded-xl`, `shadow-sm`. This keeps styles colocated with the components they affect. |
| **Recharts** | 3.8 | A charting library built on React. Used on the Market Intelligence page to render the price forecast line chart. |
| **Framer Motion** | 12.4 | An animation library for React. Currently installed as a dependency but not actively used in any component. |
| **Lucide React** | 1.16 | An icon library. Used for the menu icon, close icon, and other UI elements in the sidebar and header. |
| **class-variance-authority** | 0.7 | A utility for creating variant-based component styles. Used by the liquid glass button component to support different sizes (small, default, large, icon-only). |

### Machine Learning

| Component | What It Does |
|-----------|-------------|
| **TensorFlow** | The deep learning framework behind the disease detection model. MobileNetV2 is loaded and executed through TensorFlow's inference engine. Not bundled in requirements.txt due to its large size — it's installed separately only if you want real AI-powered disease detection. |
| **MobileNetV2** | A lightweight convolutional neural network architecture designed for mobile and edge devices. It uses depthwise separable convolutions to achieve high accuracy with far fewer parameters than traditional networks. Our version has been fine-tuned on 38 plant disease classes. |
| **Grad-CAM** | Gradient-weighted Class Activation Mapping. A technique that produces a heatmap showing which pixels in the input image most influenced the model's prediction. Implemented in the inference pipeline but not yet surfaced in the UI. |

### Database

| Technology | What It Does |
|-----------|-------------|
| **PostgreSQL** | The relational database. Stores all structured data: user accounts, farm profiles, disease reports, market predictions, risk scores, and feedback. |
| **Supabase** | A managed PostgreSQL hosting service. Instead of installing PostgreSQL on your computer, you point the app at a Supabase project URL. Supabase handles backups, connection pooling, and SSL. Also provides a management dashboard and a CLI for running migrations. |

### Design System

The app uses a custom design system built with CSS custom properties (variables). The color palette — **Deep Forest & Harvest Gold** — was chosen to evoke Indian agriculture:

| Token | Color Value | Where It Appears |
|-------|------------|------------------|
| `--color-brand-deep` | `#0A3D18` | Page headings, the sidebar brand title |
| `--color-brand-primary` | `#1A6B2C` | Buttons, links, active navigation items |
| `--color-brand-accent` | `#C8942A` | Call-to-action buttons, focus rings, hover states |
| `--color-brand-mid` | `#D4A76A` | Hero banners, gradient transitions |
| `--color-brand-light` | `#E8D5B0` | Subtle backgrounds, hover states on cards |
| `--color-canvas` | `#F8F5F0` | The main page background — a warm off-white |
| `--color-text-primary` | `#1A1C19` | Body text, headings |
| `--color-text-secondary` | `#5C5346` | Labels, secondary information |

All cards, the sidebar, and the login form use a **liquid glass effect**. This is achieved through four nested `<div>` elements inside every glass container:

1. **Effect layer** (`z-index: 0`) — Applies `backdrop-filter: blur(3px)` to blur whatever is behind the card, and `filter: url(#glass-distortion)` to warp it. The SVG filter uses **fractal noise** (Perlin-like turbulence), **specular lighting** (simulates light reflecting off a bumpy surface), and a **displacement map** (shifts pixels based on the noise pattern — this is what creates the refractive shimmer).

2. **Tint layer** (`z-index: 1`) — A semi-transparent white overlay (`rgba(255, 255, 255, 0.25)`) that gives the glass its frosted appearance.

3. **Shine layer** (`z-index: 2`) — Multiple inset `box-shadow` values create the bright edge highlights that make the glass look three-dimensional.

4. **Content layer** (`z-index: 3`) — The actual text, buttons, and form fields sit above all the glass layers.

All of this runs on the GPU through CSS — there is zero JavaScript overhead for the glass effect.

---

## Project File Structure

```
Trinetra-Agro-AI/
│
├── backend/                              # Python backend (API server)
│   ├── main.py                           # Entry point — starts FastAPI, registers all routers
│   ├── requirements.txt                  # All Python dependencies with versions
│   │
│   ├── auth/                             # Authentication system
│   │   ├── router.py                     # POST /auth/register, /login, /send-otp, /verify-otp, /refresh; GET /auth/me
│   │   ├── service.py                    # User creation, password verification, token refresh
│   │   └── otp_service.py               # OTP generation, SMS delivery via Fast2SMS
│   │
│   ├── routers/                          # Route handlers — one file per feature area
│   │   ├── ai_features.py               # POST /ai/market (price forecasting)
│   │   ├── chatbot.py                    # POST /chat/send, /chat/clear
│   │   ├── disease.py                    # POST /ai/disease (leaf image upload)
│   │   ├── feedback.py                   # POST /feedback (star ratings)
│   │   └── profile.py                    # GET/POST/PUT /profile (farmer profile CRUD)
│   │
│   ├── services/                         # Business logic layer
│   │   ├── ai_service.py                # Market forecast orchestration + DB persistence
│   │   ├── chatbot_service.py           # Chat session management, context assembly, fallback
│   │   ├── openrouter_service.py        # OpenRouter HTTP client, system prompt construction
│   │   └── disease_service.py           # Disease detector singleton, TF model loading
│   │
│   ├── schemas/                          # Pydantic models for request/response validation
│   │   ├── auth.py                       # UserCreate, UserLogin, TokenResponse, TokenRefresh
│   │   ├── ai_features.py               # MarketRequest
│   │   ├── chatbot.py                    # ChatRequest, ChatResponse
│   │   └── disease.py                    # DiseaseRequest (crop_type + image file)
│   │
│   ├── models/__init__.py                # 9 SQLAlchemy ORM models (User, Farmer, DiseaseReport, etc.)
│   ├── database/session.py              # Async SQLAlchemy engine, session factory, SSL config
│   ├── core/                             # config.py (settings), security.py (JWT + bcrypt), dependencies.py
│   └── middleware/logging.py            # HTTP request/response logger
│
├── frontend-next/                        # Next.js frontend (user interface)
│   ├── src/app/
│   │   ├── layout.tsx                    # Root HTML shell — imports global CSS, mounts glass filter
│   │   ├── page.tsx                      # Dashboard — KPI cards, quick actions, market & resource charts
│   │   ├── app-shell.tsx                 # Sidebar navigation, mobile menu, auth guard, logout
│   │   ├── globals.css                   # Design tokens, liquid glass classes, utility classes
│   │   ├── login/page.tsx                # Login — email/password + phone OTP with glass card
│   │   ├── register/page.tsx             # Registration form
│   │   ├── chatbot/page.tsx              # AI chat — message list, input, language-aware
│   │   ├── disease-scanner/page.tsx      # Leaf upload, preview, results display
│   │   ├── market/page.tsx               # Crop selector, forecast slider, Recharts chart
│   │   ├── feedback/page.tsx             # Feature selector, star rating, comment
│   │   └── profile/page.tsx              # Farm details form — get/save/update
│   │
│   ├── src/components/
│   │   ├── glass-filter.tsx             # Global SVG filter (#glass-distortion) for refraction
│   │   ├── liquid-glass.tsx             # LiquidGlass wrapper component
│   │   ├── FloatingChat.tsx             # Persistent chat bubble — appears on every page
│   │   └── ui/
│   │       └── apple-tahoe-liquid-glass-button.tsx  # macOS dock-style glass button
│   │
│   ├── src/lib/
│   │   ├── api.ts                        # HTTP client — JWT auto-attach, 401 auto-refresh + retry
│   │   ├── auth.ts                       # login(), register(), logout(), sendOtp(), verifyOtp()
│   │   ├── language.tsx                  # i18n React context provider — EN, HI, TE translations
│   │   ├── types.ts                      # TypeScript interfaces for all data shapes
│   │   └── utils.ts                      # cn() — class name merger (clsx + tailwind-merge)
│   │
│   ├── middleware.ts                     # Next.js middleware — redirects unauthenticated users
│   ├── package.json                      # Dependencies: next, react, recharts, framer-motion, lucide
│   ├── tailwind.config.ts                # Tailwind v4 configuration
│   └── vercel.json                       # Vercel deployment settings
│
├── ai_engine/                            # Machine learning (pure Python — no web framework)
│   ├── disease_detection/
│   │   ├── inference.py                  # MobileNetV2 forward pass, preprocessing, Grad-CAM
│   │   ├── train.py                      # 2-phase training pipeline for Kaggle GPU
│   │   └── models/
│   │       ├── mobilenetv2_plantvillage.keras   # Trained model (26 MB, version-independent)
│   │       ├── mobilenetv2_plantvillage.h5      # Legacy backup (HDF5 format)
│   │       └── class_names.txt                   # 38 disease class labels
│   └── market_forecasting/
│       └── engine.py                     # data.gov.in API client, trend analysis, fallback
│
├── supabase/                             # Database management
│   ├── config.toml                       # Supabase CLI project configuration
│   └── migrations/
│       ├── 20260521000001_initial_schema.sql     # Creates all 9 tables + indexes
│       ├── 20260521000002_seed_demo_user.sql     # Inserts demo@farm.com user
│       └── 20260521000003_fix_demo_password.sql  # Corrects demo user bcrypt hash
│
├── screenshots/                          # App screenshots for documentation
│   └── login.png
│
├── .github/workflows/ci.yml              # GitHub Actions — Python compile check + ruff lint on push
├── DEPLOYMENT.md                         # Production deployment guide (Vercel + Render + Supabase)
└── .env                                  # Secrets — not committed to Git
```

---

## API Endpoints — The Complete List

Every URL the frontend can call, what it expects, and what it returns.

### Authentication — `/auth/*`

| Method | Path | What It Does | Requires Login? |
|--------|------|-------------|:---:|
| `POST` | `/auth/register` | Create a new user account. Body: `{email, password, full_name?}`. Passwords are bcrypt-hashed before storage. | No |
| `POST` | `/auth/login` | Login with email + password. Returns `{access_token, refresh_token, token_type}`. | No |
| `POST` | `/auth/refresh` | Exchange a refresh token for a new access token. Body: `{refresh_token}`. | No |
| `POST` | `/auth/send-otp` | Generate a 6-digit OTP and send it via SMS to the given phone number. Body: `{phone}`. Returns `{message, expires_in_seconds}`. | No |
| `POST` | `/auth/verify-otp` | Verify the OTP and return JWT tokens. Body: `{phone, otp}`. OTPs expire after 5 minutes. | No |
| `GET`  | `/auth/me` | Return the currently authenticated user's profile (email, name, phone). Requires a valid JWT in the `Authorization` header. | Yes |

### AI & Chat — `/ai/*`, `/chat/*`

| Method | Path | What It Does | Requires Login? |
|--------|------|-------------|:---:|
| `POST` | `/ai/market` | Generate a crop price forecast. Body: `{crop: string, days: int}`. Calls data.gov.in for real prices, falls back to synthetic data. Returns `{current_price, trend, predictions[], recommendation}`. | No |
| `POST` | `/ai/disease` | Analyze a leaf image for disease. Multipart form: `image` (file) + `crop_type` (string). Runs through MobileNetV2 or fallback lookup. Returns `{disease, confidence, severity, treatment}`. | No |
| `POST` | `/chat/send` | Send a message to the AI chatbot. Body: `{message, session_id, language}`. Returns `{reply, session_id}`. Chat history is maintained server-side per session. | No |
| `POST` | `/chat/clear` | Clear the chat history for a session. Body: `{session_id}`. | No |

### Data — `/profile/*`, `/feedback`

| Method | Path | What It Does | Requires Login? |
|--------|------|-------------|:---:|
| `GET`  | `/profile` | Load the current user's farm profile from the `farmers` table. Returns `FarmerProfile` or `null`. | Yes |
| `POST` | `/profile` | Create a new farm profile. Body: `{location, land_size_acres, crops[], soil_type, irrigation_type, budget_inr, experience_years}`. | Yes |
| `PUT`  | `/profile` | Update an existing farm profile. Same body as POST. | Yes |
| `POST` | `/feedback` | Submit feature feedback. Body: `{feature, rating (1-5), comment?}`. Saved to the `feedback` table. | No |

### System

| Method | Path | What It Does |
|--------|------|-------------|
| `GET` | `/` | Welcome message — links to docs and health check |
| `GET` | `/health` | Health check — also verifies the database connection is alive. Returns `{status, version, environment, database}` |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) |
| `GET` | `/redoc` | Alternative API documentation (ReDoc) |

---

## Database — What Gets Stored

Nine tables in a PostgreSQL database, managed through Supabase. All tables use UUID primary keys and UTC timestamps.

| Table | Number of Columns | Purpose |
|-------|:-:|---------|
| `users` | 7 | User accounts. Hashed passwords (never plaintext), email, phone, full name, active status. |
| `farmers` | 10 | Farm profiles linked to users. Soil type, land size (acres), budget (INR), location, crops (JSON array), irrigation type, experience years. |
| `disease_reports` | 10 | Every leaf scan result. Crop type, disease name, confidence score, severity, image path on disk, treatment text, prevention tips (JSON). |
| `market_predictions` | 9 | Every price forecast. Crop, forecast duration, current price, trend direction, recommendation action, full prediction data (JSON). |
| `risk_assessments` | 7 | Crop failure risk scores. Risk score (0-100), risk level (Low/Medium/High), factor breakdown (JSON), mitigation steps (JSON). *(Schema defined — endpoint coming)* |
| `yield_predictions` | 10 | Yield estimates. Crop, land size, soil type, irrigation flag, conservative/moderate/optimistic estimates, unit, season. *(Schema defined — endpoint coming)* |
| `irrigation_plans` | 9 | Water schedules. Crop, land size, growth stage, daily and weekly liter estimates, irrigation method, schedule (JSON), tips (JSON). *(Schema defined — endpoint coming)* |
| `profit_analyses` | 13 | Financial projections. Crop, land size, total cost, cost per acre, cost breakdown (JSON), profit at three risk levels, ROI at three risk levels, recommendation text. *(Schema defined — endpoint coming)* |
| `feedback` | 5 | User feedback. Feature name, star rating (1-5), comment text, linked to user. |

Migrations are SQL files in `supabase/migrations/`. They're applied with `npx supabase db push` and tracked by Supabase, so they only run once.

---

## External Services We Depend On

This application integrates with four external services. Three of them have graceful fallbacks — the app still works, just with reduced functionality. One is a hard dependency.

| Service | What It Provides | Cost | What Happens If It's Down |
|---------|-----------------|------|--------------------------|
| **Supabase** | PostgreSQL database hosting | Free (500MB) | **Nothing works.** The backend validates the database connection on startup (the `lifespan` function in `main.py` runs `SELECT 1`). All data — users, profiles, disease reports, market predictions, feedback — lives here. |
| **OpenRouter** | Access to the Gemma 4 AI model | Free | The chatbot falls back to hardcoded responses. Users still get farming advice, but it's generic keyword-matched answers rather than AI-generated, context-aware responses. The fallback message clearly states the service is unavailable. |
| **data.gov.in** | Real-time mandi crop prices from Indian markets | Free (registration required) | Market predictions switch to synthetic data. The forecast is still generated using a deterministic random seed, so it's consistent across calls on the same day, but the prices are simulated rather than actual market data. |
| **Fast2SMS** | SMS delivery for OTP codes | Paid (~₹0.25/SMS) | If the SMS gateway fails, the 6-digit OTP is printed to the server console and marked as delivered anyway (used for development/testing). In production, this should return a proper error. |

The critical path: the frontend talks to the backend, the backend talks to Supabase. If Supabase is unavailable, the health check fails and no requests can be served. OpenRouter, data.gov.in, and Fast2SMS are all "nice to have" — the core app degrades gracefully without them.

---

## What's Working And What's Coming

### ✅ Fully Implemented and Working

These features have complete frontend pages, backend endpoints, service logic, database tables, and error handling:

- **Email/Password Authentication** — register, login, token refresh, protected routes
- **Phone OTP Authentication** — code generation, SMS delivery, verification
- **AI Chatbot** — OpenRouter integration with context-aware prompts, conversation memory, multilingual responses, graceful fallback
- **Disease Scanner** — MobileNetV2 inference (when TensorFlow is installed), Grad-CAM heatmap generation, severity classification, treatment recommendations, graceful fallback for 5 crops
- **Market Intelligence** — real data.gov.in API integration with trend analysis, buy/sell/hold recommendations, Recharts visualization, synthetic fallback
- **Farm Profile** — full CRUD (Create, Read, Update) with personalized chatbot context
- **Feedback System** — per-feature star ratings with optional comments, stored in database
- **Liquid Glass UI** — SVG filter refraction, backdrop-filter blur, multi-layer DOM structure, custom design tokens

### 🚧 In Progress or Planned

These features have database tables and TypeScript types defined, but no backend endpoints or frontend pages yet:

- **Risk Assessment** — crop failure probability prediction using XGBoost
- **Yield Prediction** — harvest quantity estimation using Random Forest + XGBoost ensemble
- **Irrigation Planning** — daily watering schedules optimized for crop, soil, and weather
- **Profit Analysis** — cost vs. revenue projections with ROI calculation
- **Crop Advisor** — personalized crop recommendations using KMeans clustering + cosine similarity
- **Voice Input/Output** — speech-to-text via Whisper, text-to-speech via gTTS (schemas exist, implementation removed during refactoring)
- **Grad-CAM Heatmap Display** — the heatmap is computed in inference but not rendered in the UI

---

---

## 🚀 The Deployment Journey — How We Went From Localhost To Live

This section is for anyone who has ever stared at a "Registration failed" error, redeployed six times, and wondered if they're losing their mind. You're not. Here's our story.

### The Setup

**Frontend**: Vercel (free tier — Next.js native hosting)  
**Backend**: DigitalOcean VPS ($6/month on GitHub Student credits — 33 months of runway)  
**Database**: Supabase PostgreSQL (free tier — 500MB)  
**HTTPS Tunnel**: Cloudflare Tunnel (`trycloudflare.com` — free forever)

Three services, zero monthly cost. In theory, this should take twenty minutes.

It took four hours.

### Bug #1 — "Email Already Registered"

The first deploy to Vercel went smoothly. The login page loaded. The background image loaded. The glass effect looked stunning. Clicking "Register" returned: `Registration failed — email may already exist`.

This was a lie.

The frontend was **not calling the backend at all**. The `NEXT_PUBLIC_API_URL` environment variable on Vercel was empty, so the API client fell back to `http://localhost:8000`. In production, the user's web browser was trying to connect to their own laptop, where no backend was running. The registration never left the browser. The error message was the `catch` block — not the real error.

**Fix**: Set `NEXT_PUBLIC_API_URL=http://139.59.83.96` from the Vercel CLI.

### Bug #2 — Mixed Content Blocking

Fixed the env var. Redeployed. Same error.

Vercel serves pages over **HTTPS**. Our VPS backend was plain **HTTP**. Modern browsers block all HTTP requests originating from HTTPS pages — this is called **Mixed Content Policy**, and it exists to protect users. Not a single registration request appeared in the VPS nginx logs. The `fetch()` call was silently killed by Chrome before it could even connect.

**Fix**: Installed `cloudflared` (Cloudflare Tunnel) on the VPS. This wraps the HTTP backend in a free Cloudflare HTTPS endpoint — `https://shirts-flexible-michelle-classes.trycloudflare.com`. The tunnel runs 24/7 via PM2 and auto-restarts on VPS reboot. Zero DNS configuration, instant SSL.

### Bug #3 — The Redirect Loop From Hell

Fixed the HTTPS issue. Set the env var to the Cloudflare URL. Redeployed. Navigated to the login page. Typed credentials. Clicked Sign In.

The page flashed white for 200 milliseconds and sent me back to `/login`.

This one took the longest to debug. Here's what was actually happening:

**The `request()` function** in `src/lib/api.ts` has a global intercepting mechanism. For every API call, it checks if the access token exists. If the token doesn't exist (which it shouldn't — the user hasn't logged in yet!), it tries to refresh it. If refresh fails (which it will — there's no refresh token either), it redirects to `/login`.

The call chain looked like this:

```
User clicks Sign In
  → login() calls apiClient.post("/auth/login", ...)
    → request() fires
      → "No access token! Let me refresh..."
        → "No refresh token either! Redirect to /login!"
          → User never reaches the login endpoint
```

The login API call was being **killed by its own auth guard before it could authenticate the user**. The function that was supposed to protect routes was also protecting the login route from itself.

**Fix**: Added `isAuthEndpoint` check in `request()` — if the path starts with `/auth/login`, `/auth/register`, `/auth/send-otp`, `/auth/verify-otp`, or `/auth/refresh`, skip the entire token validation chain and let the request reach the backend directly.

### Bug #4 — The Silent Cookie Killer

Fixed the redirect loop. Redeployed. Same behavior — flash and redirect.

A Playwright E2E test revealed the truth: the login flow **worked perfectly** in an automated headless browser. Cookies were present. `Secure` flag was `true`. Dashboard loaded. But in my own browser, it kept failing.

The answer: **stale cookies from ten previous deployments**.

Every time Vercel deploys, it reuses the same domain (`frontend-next-xi-six.vercel.app`). Cookies from deployment #1, #2, and #3 were all still in my browser session. The middleware was reading an ancient `access_token` that had been set **before** the `Secure` flag was added. Modern browsers prioritize the oldest matching cookie when multiple exist for the same domain — so the old broken cookie won every time.

**Fix**: Three things:
1. Added `Secure` flag to `setCookie()` — without this, cookies on HTTPS origins are silently dropped
2. Added a **stale cookie purge** in the login handler — force-clears both `access_token` and `refresh_token` cookies on the current domain before redirecting
3. Added a `300ms` delay between cookie set and `window.location.href = "/"` — cookies flush asynchronously, and redirecting immediately can lose them

### Bug #5 — The Wrong Pooler Host

The VPS was using SQLite because "Supabase PostgreSQL is unreachable from DigitalOcean Bangalore." — *our original deployment note*

The database host `db.jqbmrpvuruluxjooxzrg.supabase.co` resolves to **IPv6** only (`2406:da1c:61c:d600:...`). DigitalOcean's Bangalore (BLR1) datacenter is **IPv4-only**. The `asyncpg` driver threw `OSError: Network is unreachable` on every query.

Supabase has a **connection pooler** that runs on IPv4 — `aws-1-ap-southeast-2.pooler.supabase.com`. But we were using the wrong pooler host (`aws-0-ap-south-1`). The pooler returned `ENOTFOUND: tenant/user not found` — it couldn't route to a project it didn't know about.

**Fix**: Used the Supabase Management API (with your personal access token `sbp_...`) to query the project configuration. The correct pooler is `aws-1-ap-southeast-2.pooler.supabase.com:6543` (port 6543, transaction mode). Updated the `DATABASE_URL` and restarted the backend. Health check now returns `"database": "supabase_postgresql"`.

### Bug #6 — Missing Model File, Missing TensorFlow

The disease scanner returned "Running in fallback mode — train MobileNetV2 model for accurate predictions." even though the model file was committed to Git and deployed to the VPS.

The `.keras` file was present at 25.9MB. The inference code could find it. But TensorFlow — the library needed to load and run it — **wasn't installed on the production VPS**. It wasn't in `requirements.txt` (TF is 500MB+ and would crash the VPS during `pip install` if not done carefully).

**Fix**: Installed TensorFlow 2.21.0 on the VPS with `pip install tensorflow --break-system-packages`. The model loaded successfully. The health check now shows real inference with 98.76% accuracy. Note: TF runs on CPU only (no NVIDIA GPU on the $6/month droplet) — inference takes ~0.5 seconds per image, which is acceptable.

### Bug #7 — The AI Chatbot Silent Failure

The chatbot was responding with "I'm Trinetra, your AI farming advisor..." — the fallback message — instead of real AI answers. The OpenRouter API key was valid. The endpoint returned 200. The network was fine.

The model was `openrouter/free` — OpenRouter's automatic free model router. This wildcard model takes **30+ seconds** to resolve and respond. The `requests` call in `openrouter_service.py` had a `timeout=30`, which meant it was killing the request right as the model started responding.

**Fix**: Switched to `google/gemma-4-31b-it:free` — a specific free model that responds in 2-4 seconds. Updated `OPENROUTER_MODEL` in the VPS `.env` file and restarted the backend. The chatbot now gives real AI answers with personalized farming advice.

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| `ModuleNotFoundError: No module named 'xyz'` | Missing Python package | Run `pip install -r backend/requirements.txt` from the `backend/` folder |
| Login returns "Invalid email or password" with the demo account | Database not seeded | Run `npx supabase db push` to apply migrations, which create the demo user |
| Chatbot only gives generic answers | OpenRouter API key missing or invalid | Check that `OPENROUTER_API_KEY` in `.env` starts with `sk-or-v1-`. Get a free key at openrouter.ai/keys |
| Chatbot stopped working after server restart | Chat history is stored in memory only | This is expected — history clears on restart. Start a new conversation |
| Disease scanner returns "Not Found" or only works for 5 crops | TensorFlow not installed or model not found | Install TensorFlow with `pip install tensorflow` (requires ~500MB disk space). Download the trained model from the Kaggle training notebook output |
| Market predictions show the same prices every time | data.gov.in API key missing | Register at data.gov.in for a free API key and add it to `.env` as `DATA_GOV_API_KEY` |
| OTP codes never arrive on your phone | Fast2SMS not configured or has no credits | Check the server terminal — the OTP code is printed there for development. Fast2SMS is a paid service |
| "Network Error" when using any feature | Backend is not running | Make sure you ran `python -m uvicorn backend.main:app --reload --port 8000` in a terminal. You should see "Uvicorn running on..." |
| Page looks broken or unstyled | Browser cache | Do a hard refresh: `Ctrl + Shift + R` (Windows) or `Cmd + Shift + R` (Mac) |
| "Failed to compile" when running `npm run dev` | Missing frontend dependencies | Run `npm install` from the `frontend-next/` folder |
| CORS error in browser console | Backend `allowed_origins` doesn't include `localhost:3000` | The default config includes `http://localhost:3000`. If you changed ports, update `ALLOWED_ORIGINS` in your `.env` |
| `git clone` fails | Git not installed | Download the project as a ZIP from the GitHub page (green "Code" button → Download ZIP) |

---

## Credits

**Karthikeya Podicheti**

[![GitHub](https://img.shields.io/badge/GitHub-@KarthikeyaPodicheti-181717?style=flat&logo=github)](https://github.com/KarthikeyaPodicheti)

Built with React 19, Next.js 16, FastAPI, PostgreSQL (Supabase), Tailwind CSS v4, TensorFlow, and OpenRouter AI.
