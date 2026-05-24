# Deployment Guide — Vercel + Render (Free)

## Architecture

```
User → https://trinetra-agro.vercel.app (Vercel, free)
                  │
          Next.js Frontend (always-on)
                  │
          API calls via NEXT_PUBLIC_API_URL
                  │
                  ▼
        https://trinetra-backend.onrender.com (Render, free)
                  │
          FastAPI Backend (spins down after 15 min idle)
                  │
                  ▼
          Supabase PostgreSQL (always-on, free)
```

**Cold start behavior**: After 15 minutes of inactivity, Render spins down the backend. The first request after idle takes ~30 seconds to wake up. Subsequent requests are fast. Frontend stays instant on Vercel.

---

## Prerequisites

| Account | Where | Cost |
|---------|-------|------|
| GitHub | github.com | Free |
| Vercel | vercel.com (login with GitHub) | Free |
| Render | render.com (login with GitHub) | Free |
| Supabase | supabase.com | Free (already set up) |

---

## Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/trinetra-agro-ai.git
git push -u origin main
```

---

## Step 2: Deploy Frontend to Vercel (5 minutes)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repo
3. Set the **Root Directory** to `frontend-next`
4. Set **Framework Preset** to `Next.js`
5. Add this environment variable:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://trinetra-backend.onrender.com` |

6. Click **Deploy**
7. After deploy, Vercel gives you a URL like `https://trinetra-agro-xyz.vercel.app`

---

## Step 3: Deploy Backend to Render (10 minutes)

1. Go to [render.com](https://render.com) → **New+** → **Web Service**
2. Connect your GitHub repo
3. Configure:

| Setting | Value |
|---------|-------|
| **Name** | `trinetra-backend` |
| **Root Directory** | (leave empty — repo root) |
| **Runtime** | `Docker` |
| **Build Command** | (leave empty — uses Dockerfile) |
| **Start Command** | (leave empty — uses CMD from Dockerfile) |
| **Instance Type** | **Free** |
| **Health Check Path** | `/health` |

4. Add these environment variables:

| Variable | Value |
|----------|-------|
| `ENVIRONMENT` | `production` |
| `DATABASE_URL` | Your Supabase PostgreSQL connection string |
| `OPENROUTER_API_KEY` | `sk-or-v1-17ba...` |
| `OPENROUTER_MODEL` | `google/gemma-4-26b-a4b-it:free` |
| `SECRET_KEY` | Generate with `openssl rand -hex 32` |
| `JWT_SECRET` | Same as SECRET_KEY |

5. Click **Deploy Web Service**
6. After deploy, Render gives you a URL like `https://trinetra-backend.onrender.com`

---

## Step 4: Connect Frontend to Backend

After both are deployed:

1. Go to Vercel dashboard → Your project → **Settings** → **Environment Variables**
2. Update `NEXT_PUBLIC_API_URL` to your Render URL: `https://trinetra-backend.onrender.com`
3. Go to **Deployments** → trigger a **Redeploy**

---

## Step 5: Custom Domain (Optional)

**Vercel**: Settings → Domains → add your domain. Vercel handles SSL automatically.

**Render**: Settings → Custom Domain → add domain. Render provides SSL via Let's Encrypt.

---

## Free Tier Limitations

| Platform | Limit | Impact |
|----------|-------|--------|
| **Vercel** | 100 GB bandwidth/month | Fine for personal/demo use |
| **Vercel** | 6000 build minutes/month | Plenty |
| **Render** | Backend sleeps after **15 min idle** | First request after idle = ~30s cold start |
| **Render** | 750 hours/month (≈24h/day, 31 days) | Runs continuously if traffic every <15 min |
| **Render** | 100 GB outbound bandwidth | Fine |
| **Supabase** | 500 MB database | Plenty |
| **Supabase** | 50,000 monthly active users | More than enough |

---

## Handling the Cold Start

**Option A: Uptime monitor (free)**

Use [uptimerobot.com](https://uptimerobot.com) (free tier) to ping Render's `/health` endpoint every 14 minutes. This keeps the backend warm indefinitely. UptimeRobot free tier monitors 5 URLs at 5-minute intervals.

**Option B: Accept it**

Add a loading state in the frontend. On first load, show "Waking up the AI engine..." while the backend boots. This takes ~30 seconds once, then fast for the next 15 minutes.

**Option C: Render Blaze ($7/month)**

Upgrade Render to the Starter plan ($7/month) for:
- Zero cold starts
- Always-on
- 512MB RAM
- Dedicated CPU
- Priority support

---

## Updating After Deployment

```bash
git add .
git commit -m "fix: update something"
git push origin main
```

**Vercel** auto-deploys on push to main branch (detects changes in `frontend-next/`).

**Render** auto-deploys on push to main branch (detects Dockerfile changes).

---

## Verifying the Deployment

| Check | URL | Expected |
|-------|-----|----------|
| Frontend | `https://trinetra-agro-xyz.vercel.app` | Login page loads |
| Backend health | `https://trinetra-backend.onrender.com/health` | `{"status":"healthy"}` |
| Backend docs | `https://trinetra-backend.onrender.com/docs` | Swagger UI |
| Login | Frontend → login with `demo@farm.com` | Redirects to dashboard |
| AI Advisor | Frontend → fill form → submit | Returns recommendations |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Frontend loads but API calls fail | `NEXT_PUBLIC_API_URL` wrong | Check env var in Vercel dashboard |
| "Network Error" on login | Backend is sleeping | Wait 30s and retry, or set up uptime monitor |
| Backend deploy fails | Docker build timeout on free tier | Free tier has 5 min build limit; if exceeded, upgrade or remove heavy deps |
| Auth not working | `SECRET_KEY` mismatch | Ensure same key on Render and in deployed config |
| CORS errors | Backend `allowed_origins` doesn't include Vercel URL | Update `allowed_origins` in `backend/core/config.py` or set `ALLOWED_ORIGINS` env var |

---

## File: `frontend-next/vercel.json`

Create this file in the repo root for Vercel configuration:

```json
{
  "buildCommand": "cd frontend-next && npm run build",
  "outputDirectory": "frontend-next/.next",
  "installCommand": "cd frontend-next && npm install",
  "framework": "nextjs"
}
```

> **Note**: In the Vercel dashboard, set **Root Directory** to `frontend-next` instead of using the above config. The vercel.json above assumes repo-root setup. The simpler approach is setting Root Directory in the UI.
