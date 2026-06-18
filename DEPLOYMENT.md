# Deployment Guide — Vercel + DigitalOcean VPS + Cloudflare Tunnel

## Architecture

```
User → https://trinetra-agro.vercel.app (Vercel, free)
                  │
          Next.js Frontend (always-on, global CDN)
                  │
          API calls via Cloudflare Tunnel URL
          (NEXT_PUBLIC_API_URL)
                  │
                  ▼
    https://shirts-flexible-michelle-classes.trycloudflare.com
                  │
           Cloudflare Tunnel (cloudflared, free)
                  │
                  ▼
          DigitalOcean VPS (Docker)
          │
          ├── nginx:80 (reverse proxy)
          ├── backend:8000 (FastAPI via uvicorn)
          └── Never cold-starts — always-on VPS
                  │
                  ▼
          Supabase PostgreSQL (always-on, free)
```

**No cold start**: Unlike Render, the DigitalOcean VPS runs 24/7 — the backend is always warm. Zero delay on first request.

---

## Prerequisites

| Account | Where | Cost |
|---------|-------|------|
| GitHub | github.com | Free |
| Vercel | vercel.com (login with GitHub) | Free |
| DigitalOcean | digitalocean.com | $6/month (GitHub Student credits available) |
| Cloudflare | cloudflare.com | Free (Tunnel feature) |
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
   | `NEXT_PUBLIC_API_URL` | Your Cloudflare Tunnel URL (see Step 5) |

6. Click **Deploy**
7. After deploy, Vercel gives you a URL like `https://trinetra-agro.vercel.app`

The `frontend-next/vercel.json` config is already set up for this.

---

## Step 3: Set Up the DigitalOcean VPS (15 minutes)

### 3a — Create a Droplet

1. Go to [cloud.digitalocean.com](https://cloud.digitalocean.com) → Create → Droplet
2. Choose **Ubuntu 24.04 LTS**
3. Plan: **Basic** → **Regular with SSD** → **$6/month** (1 GB RAM, 1 CPU, 25 GB SSD)
4. Add your SSH key for passwordless login
5. Create the droplet — note the IP address

### 3b — Install Docker

SSH into the VPS and run:

```bash
# Update system
apt update && apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose plugin
apt install -y docker-compose-plugin
```

### 3c — Clone the repo and start services

```bash
git clone https://github.com/YOUR_USERNAME/trinetra-agro-ai.git
cd trinetra-agro-ai/Trinetra-Agro-AI

# Create .env with all secrets
cat > .env << 'EOF'
ENVIRONMENT=production
DATABASE_URL=postgresql+asyncpg://postgres.YOUR_REF:YOUR_PASSWORD@aws-1-ap-southeast-2.pooler.supabase.com:6543/postgres
SECRET_KEY=your-openssl-generated-secret
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxx
OPENROUTER_MODEL=google/gemma-4-26b-a4b-it:free
DATA_GOV_API_KEY=your-data-gov-key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost,https://trinetra-agro.vercel.app
EOF

# Start with Docker Compose
docker compose up -d

# Verify everything is running
docker compose ps
```

The `Dockerfile`, `nginx.conf`, and `docker-compose.yml` are already configured in the repo. Nginx runs on port 80 and routes:

| Path | Destination |
|------|-------------|
| `/api`, `/auth`, `/ai`, `/chat`, `/profile`, `/feedback`, `/health`, `/docs` | Backend (`backend:8000`) |
| `/` (everything else) | Frontend (`frontend:3000`) |

### 3d — Install PM2 for cloudflared auto-restart

```bash
# Install Node.js + PM2
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
npm install -g pm2

# Start cloudflared via PM2 (so it auto-restarts on reboot)
pm2 start cloudflared -- tunnel --url http://localhost:80
pm2 save
pm2 startup  # Follow the instructions to enable startup
```

---

## Step 4: Install & Configure Cloudflare Tunnel (5 minutes)

**Why this is needed**: Vercel serves pages over HTTPS, but the VPS backend is plain HTTP. Modern browsers block HTTP requests from HTTPS pages (mixed content policy). Cloudflare Tunnel wraps the HTTP backend in a free HTTPS endpoint.

1. Install `cloudflared` on the VPS:

   ```bash
   curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
   chmod +x /usr/local/bin/cloudflared
   ```

2. Start the tunnel (connected via PM2 — see Step 3d):

   ```bash
   cloudflared tunnel --url http://localhost:80
   ```

3. The tunnel prints a URL like:
   ```
   https://shirts-flexible-michelle-classes.trycloudflare.com
   ```

4. Copy this URL and update the **Vercle environment variable** `NEXT_PUBLIC_API_URL` to this URL. Also update `frontend-next/src/lib/api.ts`'s fallback URL.

---

## Step 5: Connect Frontend to Backend

1. Go to Vercel dashboard → Your project → **Settings** → **Environment Variables**
2. Set `NEXT_PUBLIC_API_URL` to your Cloudflare Tunnel URL: `https://shirts-flexible-michelle-classes.trycloudflare.com`
3. Go to **Deployments** → trigger a **Redeploy**

---

## Step 6: Apply Database Migrations

```bash
# From the Trinetra-Agro-AI/ directory, with Supabase CLI installed:
npx supabase db push
```

This creates all 9 tables in your Supabase PostgreSQL database and seeds the demo user (`demo@farm.com` / `demo123456`).

---

## Updating After Deployment

```bash
# On your local machine:
git add .
git commit -m "feat: update something"
git push origin main

# On the VPS:
cd trinetra-agro-ai/Trinetra-Agro-AI
git pull origin main
docker compose down
docker compose up -d --build
```

**Vercel** auto-deploys on push to main branch (detects changes in `frontend-next/`).

---

## Verifying the Deployment

| Check | URL | Expected |
|-------|-----|----------|
| Frontend | `https://trinetra-agro.vercel.app` | Login page loads |
| Backend health (via tunnel) | `https://shirts-flexible-michelle-classes.trycloudflare.com/health` | `{"status":"healthy"}` |
| Backend docs (via tunnel) | `https://shirts-flexible-michelle-classes.trycloudflare.com/docs` | Swagger UI |
| Login | Frontend → login with `demo@farm.com` | Redirects to dashboard |
| Disease Scanner | Frontend → upload leaf image | Returns disease diagnosis |

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Frontend loads but API calls fail | Cloudflare Tunnel URL wrong or tunnel not running | On VPS: `pm2 status` to check cloudflared, then update `NEXT_PUBLIC_API_URL` in Vercel |
| "Mixed Content" error in browser | Tunnel is down, HTTP being used from HTTPS page | Restart cloudflared: `pm2 restart cloudflared` |
| Backend returns 502 | Docker containers not running | On VPS: `docker compose ps` — restart with `docker compose up -d` |
| Auth not working | `SECRET_KEY` mismatch | Ensure same key on VPS `.env` and in deployed config |
| CORS errors | Backend `ALLOWED_ORIGINS` doesn't include Vercel URL | Update `ALLOWED_ORIGINS` in VPS `.env` and restart: `docker compose restart` |
| Disease scanner not working | TensorFlow not installed in Docker container | SSH into VPS, exec into container: `docker compose exec backend pip install tensorflow --break-system-packages` then restart |
| Chatbot gives generic fallback answers | OpenRouter API key missing or wrong model | Check `OPENROUTER_API_KEY` and `OPENROUTER_MODEL=google/gemma-4-26b-a4b-it:free` in VPS `.env` |
| Database connection fails | Wrong pooler host in `DATABASE_URL` | Use Supabase's IPv4-compatible pooler: `aws-1-ap-southeast-2.pooler.supabase.com:6543` (transaction mode) |

---

## Free Tier Costs Breakdown

| Service | Cost | Details |
|---------|------|---------|
| Vercel | Free | 100 GB bandwidth, 6000 build minutes/month |
| DigitalOcean | $6/month | 1 GB RAM, 1 CPU, 25 GB SSD |
| Cloudflare Tunnel | Free | Unlimited bandwidth |
| Supabase | Free | 500 MB database, 50,000 monthly active users |
| **Total** | **$6/month** | Can be $0 with GitHub Student credits |

---

## Alternative: Local Development (No Cloud Needed)

For local testing without deploying:

```bash
# Terminal 1 — Start backend
cd Trinetra-Agro-AI
python -m uvicorn backend.main:app --reload --port 8000

# Terminal 2 — Start frontend
cd Trinetra-Agro-AI/frontend-next
npm run dev

# Open http://localhost:3000
```
