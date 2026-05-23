# Trinetra Agro AI — Frontend Migration: Streamlit → Next.js

## Understanding Summary

- **What:** Replace the Streamlit frontend with Next.js (TypeScript + Tailwind + App Router). FastAPI backend, AI engines, and Supabase database stay unchanged.
- **Why:** Production-ready UI with SSR, type safety, responsive design, proper routing, and modern DX — without touching the working Python backend.
- **Who:** Indian farmers accessing via web on mobile and desktop.
- **Constraints:** FastAPI (port 8000) is the single data layer. No Prisma, no direct DB access from Next.js. JWT tokens managed client-side. 6 existing pages must be replicated exactly.
- **Non-goals:** No backend changes. No AI engine changes. No database migration. No voice AI on the frontend (stays on FastAPI).

## Assumptions

- Next.js App Router with TypeScript and Tailwind CSS
- `fetch()` API for all backend calls via a thin wrapper (`lib/api.ts`)
- JWT tokens in `localStorage` with `middleware.ts` for auth gating
- Deploy on Vercel; FastAPI deploys separately (unchanged)
- Recharts for charts, lucide-react for icons
- Mobile-first responsive design
- No state management library (local state + React context is sufficient)

## Decision Log

| Decision | Alternatives Considered | Why |
|----------|------------------------|-----|
| FastAPI as sole backend | Add Prisma for direct DB reads | AI engines are Python-only; 2 ORMs = more maintenance |
| No state management lib | Zustand, Jotai | 6 pages with local state — not warranted |
| Recharts over Plotly.js | Plotly.js, Chart.js | React-native, tree-shakeable, matches chart types needed |
| Native `fetch` | axios | Thin wrapper is sufficient; one fewer dependency |
| `middleware.ts` for auth | useEffect-based gate | Prevents flash of unauthenticated content |

## Architecture

```
┌──────────────────────────────────────────────────┐
│                   Next.js (Vercel)               │
│                                                   │
│  App Router                                       │
│  ├── layout.tsx         (auth gate + nav shell)  │
│  ├── page.tsx           (dashboard)              │
│  ├── login/page.tsx                              │
│  ├── register/page.tsx                           │
│  ├── advisor/page.tsx                            │
│  ├── disease-scanner/page.tsx                    │
│  ├── market/page.tsx                             │
│  ├── chatbot/page.tsx                            │
│  └── feedback/page.tsx                           │
│                                                   │
│  lib/                                             │
│  ├── api.ts              (fetch wrapper + JWT)   │
│  ├── auth.ts             (login/register/logout)  │
│  └── types.ts            (shared TypeScript)     │
└──────────────┬───────────────────────────────────┘
               │ HTTPS + JWT
┌──────────────▼───────────────────────────────────┐
│              FastAPI (unchanged)                  │
│  Port 8000 — 18 endpoints                        │
│  8 AI engines — Python-only                      │
│  Supabase PostgreSQL — 9 tables                  │
└──────────────────────────────────────────────────┘
```

## Pages & Components

| Page | Route | Components | Fetch | State |
|------|-------|-----------|-------|-------|
| Login | `/login` | `LoginForm`, `RegisterForm` | POST `/auth/login`, `/auth/register` | Form only |
| Dashboard | `/` (default) | `KpiCards`, `QuickActions`, `MarketChart`, `ResourceChart`, `FarmingTips` | ISR 300s + client fetch | Local |
| Advisor | `/advisor` | `FarmForm`, `CropCard`, `RoiMetrics` | POST `/ai/advisor` | Form + result |
| Disease Scanner | `/disease-scanner` | `ImageUploader`, `CropSelect`, `DiagnosisCard`, `TreatmentCard`, `PreventionList` | POST `/ai/disease` (multipart) | File + result |
| Market | `/market` | `MarketForm`, `PriceChart`, `RecommendationBanner`, `TrendCards` | POST `/ai/market` | Form + result |
| Chatbot | `/chatbot` | `ChatMessage[]`, `ChatInput`, `ClearButton` | POST `/chat/send` | Local array |
| Feedback | `/feedback` | `FeedbackForm` (feature/rating/comment) | POST (TBD) | Form |

## Data Flow

### Auth Flow
```
Login form → POST /auth/login → tokens → localStorage
                                       ↓
middleware.ts reads localStorage → valid? → render
                                  expired? → POST /auth/refresh → retry
                                  both expired? → redirect /login
```

### API Call Flow
```
Page component → apiClient.post(path, data)
                       ↓
       check token expiry → refresh if needed
                       ↓
       fetch() to FastAPI with Bearer header
                       ↓
       returns JSON → component renders
                       ↓
       error? → ErrorBanner with retry
```

## Packages

```
next, react, react-dom    — framework
typescript                — types
tailwindcss               — styling
recharts                  — charts
lucide-react              — icons
```

That's it. No axios, no zustand, no react-query.

## Migration Plan — 5 Phases

### Phase 1: Scaffold + Auth
- `create-next-app` with `--typescript --tailwind --app --src-dir`
- Install `recharts`, `lucide-react`
- Create `src/lib/api.ts` (fetch wrapper with JWT refresh)
- Create `src/lib/auth.ts` (login, register, logout, token helpers)
- Create `src/lib/types.ts` (all TypeScript interfaces for API contracts)
- Add `src/middleware.ts` (auth redirect guard reading from localStorage)
- Create login and register pages
- **Test:** Login flow works end-to-end

### Phase 2: Dashboard
- Create `/` page with KPI cards, quick actions, mini charts, tips
- **Test:** Page renders, placeholder data flows

### Phase 3: Advisor + Market
- Create `/advisor` — farm form → POST → crop recommendation cards + ROI metrics
- Create `/market` — crop/days form → POST → PriceChart + trend + recommendation
- **Test:** Both forms submit and display AI results

### Phase 4: Disease Scanner + Chatbot + Feedback
- Create `/disease-scanner` — image upload + crop select → diagnosis card
- Create `/chatbot` — message history + input + clear
- Create `/feedback` — feature/rating/comment form
- **Test:** All pages function

### Phase 5: Polish
- Mobile responsive (sidebar → hamburger on small screens)
- Loading skeletons on every page
- Error states + retry for every API call
- Dark mode (Tailwind class-based)
- Vercel deployment

## API Endpoints Reference (unchanged)

| Method | Path | Auth | Body | Response |
|--------|------|------|------|----------|
| POST | `/auth/register` | No | email, password, full_name | TokenResponse |
| POST | `/auth/login` | No | email, password | TokenResponse |
| POST | `/auth/refresh` | No | refresh_token | TokenResponse |
| GET | `/auth/me` | JWT | — | UserResponse |
| POST | `/ai/advisor` | Optional | soil_type, land_acres, budget, season | recommendations |
| POST | `/ai/market` | Optional | crop, days, location | forecast + recommendation |
| POST | `/ai/disease` | Optional | crop_type, image (multipart) | diagnosis + treatment |
| POST | `/chat/send` | Optional | message, session_id | ChatResponse |
| POST | `/chat/clear` | No | session_id | status |
| GET | `/health` | No | — | status |
| GET | `/` | No | — | welcome |
