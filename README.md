# 🔱 Trinetra Agro AI

> An AI-powered farming assistant web app that helps farmers with crop recommendations, disease detection, market price forecasting, and more — through a simple chat-based interface.

---

## 📋 Table of Contents

1. [What This App Does](#-what-this-app-does)
2. [How It Works (Simple Explanation)](#-how-it-works-simple-explanation)
3. [Project Structure](#-project-structure)
4. [Setup Guide (Step-by-Step for Beginners)](#-setup-guide-step-by-step-for-beginners)
5. [Running the App](#-running-the-app)
6. [How Every Feature Works](#-how-every-feature-works)
7. [Tech Stack Explained](#-tech-stack-explained)
8. [API Reference](#-api-reference)
9. [Troubleshooting](#-troubleshooting)

---

## 🌾 What This App Does

**Trinetra Agro AI** is a web application built for Indian farmers. It has **6 main pages**:

| Page | What it does |
|------|-------------|
| 📊 **Dashboard** | Home screen with quick stats and farming tips |
| 🌱 **AI Advisor** | Enter your soil, land, budget → get best crop recommendations |
| 🔬 **Disease Scanner** | Upload a photo of a sick plant → AI tells you the disease + cure |
| 📈 **Market Intelligence** | See price forecasts for crops like wheat, rice, cotton |
| 💬 **AI Chatbot** | Ask farming questions in plain English, get instant AI answers |
| 📝 **Feedback** | Submit feedback about the app |

---

## 🧠 How It Works (Simple Explanation)

Think of this app as having **two parts** that talk to each other:

```
┌─────────────────────────────────────────────────────────────────┐
│                        YOUR BROWSER                              │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐  │
│   │          FRONTEND  (Streamlit — port 8501)               │  │
│   │   What you see and click on                              │  │
│   │   Like the "face" of the app                             │  │
│   └──────────────────┬───────────────────────────────────────┘  │
│                      │  sends requests (HTTP)                    │
│   ┌──────────────────▼───────────────────────────────────────┐  │
│   │          BACKEND   (FastAPI — port 8000)                 │  │
│   │   The "brain" — handles logic, AI, database              │  │
│   │   Talks to: AI engines, Supabase database, OpenRouter    │  │
│   └──────────────────────────────────────────────────────────┘  │
│                                                                  │
│   ┌────────────────┐    ┌────────────────┐                       │
│   │  Supabase DB   │    │  OpenRouter AI │                       │
│   │  (cloud data)  │    │  (chatbot LLM) │                       │
│   └────────────────┘    └────────────────┘                       │
└─────────────────────────────────────────────────────────────────┘
```

**In plain English:**
- You open the app at `http://localhost:8501`
- You click a button or type a question
- The frontend sends that to the backend at `http://localhost:8000`
- The backend runs AI logic and returns an answer
- The frontend shows you the result

---

## 📁 Project Structure

```
Trinetra-Agro-AI/
│
├── 📂 frontend/                  ← What the user sees (Streamlit UI)
│   ├── app.py                    ← Main app file, login screen, navigation
│   ├── api_client.py             ← Sends HTTP requests to backend
│   ├── requirements.txt          ← Frontend dependencies
│   └── 📂 views/                 ← One file per page
│       ├── dashboard.py          ← Home page
│       ├── advisor.py            ← AI Crop Advisor page
│       ├── disease.py            ← Disease Scanner page
│       ├── market.py             ← Market Intelligence page
│       ├── chatbot.py            ← AI Chatbot page
│       └── feedback.py           ← Feedback page
│
├── 📂 backend/                   ← The "brain" (FastAPI API server)
│   ├── main.py                   ← Starts the backend server
│   ├── requirements.txt          ← Backend dependencies
│   ├── 📂 auth/                  ← Login, register, JWT tokens
│   ├── 📂 core/                  ← Settings, security, config
│   ├── 📂 database/              ← Database connection
│   ├── 📂 models/                ← Database table definitions
│   ├── 📂 routers/               ← API route handlers
│   ├── 📂 schemas/               ← Data validation
│   └── 📂 services/              ← Business logic
│
├── 📂 ai_engine/                 ← Pure AI/ML logic (no web code)
│   ├── market_forecasting/       ← Price prediction engine
│   ├── recommendation_engine/    ← Crop advisor engine
│   └── disease_detection/        ← Plant disease analyzer
│
├── 📂 supabase/                  ← Cloud database setup
│   └── 📂 migrations/            ← SQL scripts that create tables
│
├── .env                          ← Secret keys and database URL (DO NOT SHARE)
└── README.md                     ← This file
```

---

## 🚀 Setup Guide (Step-by-Step for Beginners)

> **Time needed:** About 15–20 minutes  
> **Difficulty:** Beginner — just follow each step carefully

---

### Step 1 — Install Python 3.9

> ⚠️ This project requires **Python 3.9 specifically**. Other versions may not work.

1. Go to: https://www.python.org/downloads/release/python-3913/
2. Scroll down, click **"Windows installer (64-bit)"**
3. Run the installer
4. ✅ **IMPORTANT:** Check the box that says **"Add Python to PATH"** before clicking Install
5. Click **Install Now**

**Verify it worked** — open Command Prompt and type:
```
py -3.9 --version
```
You should see: `Python 3.9.x`

---

### Step 2 — Install Git

1. Go to: https://git-scm.com/download/windows
2. Download and run the installer (keep all default settings, just click Next)

**Verify it worked:**
```
git --version
```
You should see something like: `git version 2.x.x`

---

### Step 3 — Clone the Project

Open **Command Prompt** (press Windows key, type "cmd", press Enter) and run:

```bash
git clone https://github.com/KarthikeyaPodicheti/Trinetra-Agro-AI.git
```

Then navigate into the folder:
```bash
cd Trinetra-Agro-AI
```

> 💡 **What is `cd`?** It means "change directory" — it takes you inside the project folder.

---

### Step 4 — Create the `.env` File

The app needs a file called `.env` that contains secret keys (API keys, database password). This file is **not on GitHub** for security reasons — you need to create it yourself.

1. Inside the `Trinetra-Agro-AI` folder, create a new file named exactly `.env` (with the dot)
2. Copy and paste this content into it:

```env
# OpenRouter API Key (powers the AI chatbot)
# Get this from your teammate Uday — do NOT put real keys in public files
OPENROUTER_API_KEY=your-openrouter-api-key-here
OPENROUTER_MODEL=google/gemma-4-26b-a4b-it:free

# Database (Supabase PostgreSQL - already set up in the cloud)
# Get this connection string from your teammate Uday
DATABASE_URL=your-supabase-database-url-here

# Supabase Details
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_PROJECT_REF=your-project-ref

# App Settings
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=trinetra-agro-ai-dev-secret-key-change-in-production
REQUIRE_LOGIN=false
```

> 🔐 **Get the real values from your teammate (Uday).** He will share the actual `.env` file privately (via WhatsApp/email) — never put real API keys on GitHub!

> 💡 **How to create this file:**
> - Open Notepad
> - Paste the content above
> - Click File → Save As
> - Navigate to the `Trinetra-Agro-AI` folder
> - Change "Save as type" to "All Files"
> - Name it `.env` (with the dot, no .txt extension)
> - Click Save

---

### Step 5 — Install Backend Dependencies

In Command Prompt (make sure you're still inside `Trinetra-Agro-AI`):

```bash
py -3.9 -m pip install -r backend/requirements.txt
```

> ⏳ This will download about 20+ packages. It may take 3–5 minutes. Wait for it to finish.

---

### Step 6 — Install Frontend Dependencies

```bash
py -3.9 -m pip install -r frontend/requirements.txt
```

> ⏳ This is faster — only 3 packages. Should finish in under a minute.

---

### Step 7 — Verify Everything Installed

```bash
py -3.9 -c "import fastapi, streamlit, httpx; print('All good!')"
```

You should see: `All good!`

---

## ▶️ Running the App

You need to open **two separate Command Prompt windows** — one for the backend, one for the frontend.

### Terminal 1 — Start the Backend

```bash
cd Trinetra-Agro-AI
py -3.9 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

✅ You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

> Keep this window open. **Do not close it.**

---

### Terminal 2 — Start the Frontend

Open a **new** Command Prompt window and run:

```bash
cd Trinetra-Agro-AI
py -3.9 -m streamlit run frontend/app.py --server.port 8501
```

✅ You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

### Open the App

Open your browser and go to: **http://localhost:8501**

**Login credentials:**
```
Email:    demo@farm.com
Password: demo123456
```

---

## 🔍 How Every Feature Works

### 🌱 AI Advisor — How does it recommend crops?

**You enter:** Soil type, land size, budget, season  
**It does:** Runs a scoring algorithm that matches your farm conditions against a database of 20+ crops  
**It returns:** Top 3–5 crops with match score, profit estimate, water needs, and disease risks

**Code location:** `ai_engine/recommendation_engine/engine.py`

The engine scores each crop on:
- Does it match your soil type? (+points)
- Is it the right season (Kharif/Rabi)? (+points)
- Do you have enough budget? (+points)
- Is irrigation available? (+points)

---

### 🔬 Disease Scanner — How does it detect disease?

**You upload:** A photo of a sick plant  
**It does:** Uses OpenCV (computer vision) to analyze color patterns, texture, and spots in the image  
**It returns:** Disease name, confidence score, severity, treatment steps, prevention tips

**Code location:** `ai_engine/disease_detection/inference.py`

The analyzer looks at:
- Color signatures (yellowing = nutrient deficiency, brown spots = fungal infection)
- Texture irregularities
- Spot patterns on leaves

> 💡 **Note:** This uses a rule-based computer vision system (not a trained deep learning model), so it works without a GPU.

---

### 📈 Market Intelligence — Where do the prices come from?

**You select:** Crop + forecast days (7–30 days)  
**It does:** Uses a statistical model (moving average + random walk simulation) to predict price trends  
**It returns:** Daily price forecast chart, buy/sell/hold recommendation

**Code location:** `ai_engine/market_forecasting/engine.py`

The engine uses:
- Real base prices from government MSP data (hardcoded)
- A seeded random walk simulation (consistent for the same day)
- 7-day moving average to smooth out noise

> 💡 **Note:** Prices are simulated (not live market data) since we don't have a paid market API. The trends are realistic and useful for demonstration.

---

### 💬 AI Chatbot — How does it answer questions?

**You type:** Any farming question in English  
**It does:** Sends your message to OpenRouter AI (a free AI API), gets a farming-focused answer  
**It returns:** An intelligent text response

**Code location:** `backend/services/chatbot_service.py` + `backend/services/openrouter_service.py`

The chatbot:
1. Takes your message
2. Adds a system prompt: *"You are an expert Indian farming assistant..."*
3. Sends it to the AI model via OpenRouter API
4. Returns the AI's response
5. Maintains chat history within your session

**AI Model used:** `google/gemma-4-26b-a4b-it:free` (free tier via OpenRouter)

---

### 🔐 Login System — How does authentication work?

When you log in:
1. You send email + password to `/auth/login`
2. Backend checks your password against the hashed password in the database
3. If correct, it creates two tokens:
   - **Access Token** (valid for 30 minutes) — lets you use the app
   - **Refresh Token** (valid for 7 days) — lets you get a new access token
4. These tokens are stored in your browser session
5. Every time you click something, the token is sent to the backend to verify you're logged in

This is called **JWT (JSON Web Token) authentication** — the industry standard for web apps.

---

## 🛠️ Tech Stack Explained

| Layer | Technology | What it does | Why we use it |
|-------|-----------|--------------|---------------|
| **Frontend** | Streamlit | Builds the UI in Python | Simple to write, no HTML/CSS needed |
| **Backend** | FastAPI | API server | Fast, modern, automatic docs |
| **Database** | Supabase (PostgreSQL) | Stores users, analyses | Free cloud database |
| **AI Chat** | OpenRouter + Gemma | Powers the chatbot | Free AI API |
| **Auth** | JWT tokens | Secure login | Industry standard |
| **ORM** | SQLAlchemy | Talks to database | Pythonic database access |
| **HTTP** | httpx | Frontend talks to backend | Async HTTP client |

### Why Two Separate Servers?

Most web apps have a **frontend** (what you see) and a **backend** (the logic). We split them so:
- The backend can be deployed on a server (like AWS, Heroku)
- The frontend can be deployed separately (like Streamlit Cloud)
- Other apps could also use the backend API (e.g., a mobile app)

---

## 📡 API Reference

The backend exposes these endpoints. You can view them at **http://localhost:8000/docs**

### Authentication
| Method | URL | What it does |
|--------|-----|-------------|
| POST | `/auth/register` | Create a new account |
| POST | `/auth/login` | Login, get tokens |
| POST | `/auth/refresh` | Get new access token |
| GET  | `/auth/me` | Get your profile |

### AI Features
| Method | URL | What it does |
|--------|-----|-------------|
| POST | `/ai/advisor` | Get crop recommendations |
| POST | `/ai/market` | Get price forecast |
| POST | `/chat/send` | Send a chatbot message |
| POST | `/chat/clear` | Clear chat history |
| POST | `/disease/analyze` | Analyze plant disease from image |

### System
| Method | URL | What it does |
|--------|-----|-------------|
| GET | `/health` | Check if backend is running |
| GET | `/docs` | Interactive API documentation |

---

## 🔧 Troubleshooting

### ❌ "py is not recognized as a command"
You forgot to check "Add Python to PATH" during installation.  
**Fix:** Reinstall Python and tick that checkbox.

---

### ❌ "ModuleNotFoundError: No module named 'fastapi'"
Dependencies aren't installed.  
**Fix:** Run `py -3.9 -m pip install -r backend/requirements.txt` again.

---

### ❌ "Address already in use" on port 8000 or 8501
Another process is using that port.  
**Fix:** Close all Command Prompt windows, wait 10 seconds, try again.

---

### ❌ "Connection refused" — Frontend can't reach backend
The backend isn't running.  
**Fix:** Make sure Terminal 1 (backend) is still open and running.

---

### ❌ Chatbot says "connection error"
The backend isn't running or the `.env` file is missing the API key.  
**Fix:**
1. Check Terminal 1 is still running
2. Check your `.env` file has `OPENROUTER_API_KEY=...`

---

### ❌ Login fails with "Invalid email or password"
Demo user might not exist in the database.  
**Fix:** Try registering a new account using the Register tab on the login screen.

---

## 👥 Team

Built by Uday and team as part of our engineering project.

- **Demo Login:** `demo@farm.com` / `demo123456`
- **GitHub:** https://github.com/KarthikeyaPodicheti/Trinetra-Agro-AI
- **Backend API Docs:** http://localhost:8000/docs (when running locally)

---

## 📌 Quick Reference Card

```
START APP:
  Terminal 1: py -3.9 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
  Terminal 2: py -3.9 -m streamlit run frontend/app.py --server.port 8501

OPEN APP:   http://localhost:8501
API DOCS:   http://localhost:8000/docs
LOGIN:      demo@farm.com / demo123456

INSTALL:
  py -3.9 -m pip install -r backend/requirements.txt
  py -3.9 -m pip install -r frontend/requirements.txt
```