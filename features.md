# New Features — Implementation Plan

## Overview

Five features that solve real problems for Indian small/marginal farmers. Each feature targets a specific pain point with measurable financial impact. Implementation order below is priority order — each feature builds on the previous.

| Feature | Pain Point Solved | Financial Impact | Time to Build |
|---------|-------------------|-----------------|---------------|
| Live Mandi Prices | Middlemen underpay by 15-30% | ₹3,000-6,000/crop cycle | 2-3 hours |
| Weather Spray Alerts | Pesticide washed off by rain | ₹500-2,000/wasted spray | 3-4 hours |
| Government Scheme Eligibility | ₹6,000/year PM-KISAN unclaimed | ₹6,000/year free money | 4-5 hours |
| Mandi Comparison | Selling at nearest, not best | ₹200-500/quintal gain | 2-3 hours |

---

## Feature 1: Live Mandi Prices from data.gov.in

### Problem
Current market page shows hardcoded demo data for 2 crops (Wheat/Rice). When a real farmer looks at this, they make selling decisions based on fake numbers. This is worse than no data — it actively harms.

### What Changes
Replace the entire `/market` page with real-time data from the government's Open Data API. The user types a crop name, selects their state and district, and sees actual mandi prices from the last 7 days with a buy/sell/hold recommendation.

### Technical Implementation

**Backend** — New file: `backend/routers/mandi.py`

```
Endpoint: GET /api/mandi/prices?crop=tomato&state=Andhra+Pradesh&district=Kurnool
```

- Calls `https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070` (Government Mandi Price API)
- Parameters: `api-key`, `format=json`, `filters[commodity]`, `filters[state]`, `filters[district]`, `limit=30`
- Returns: `{ prices: [{mandi, crop, price_per_quintal, date, arrival_tonnes}], trend: "rising"|"falling"|"stable", recommendation: "sell_now"|"wait"|"hold" }`
- Trend calculated from 7-day moving average slope
- Recommendation: rising trend + above avg → hold, falling + below avg → sell_now

**Frontend** — Update `frontend-next/src/app/market/page.tsx`
- Remove static charts with fake data
- Add: crop search input (typeahead with autocomplete from the API's commodity list)
- Add: state + district dropdowns (load from API)
- Show: price card — current ₹/quintal with up/down arrow and % change
- Show: 7-day mini line chart (Plotly or recharts, already installed)
- Show: "Sell now at __ mandi for ₹__/quintal" or "Wait — prices rising ~2%/day"

**Dependencies Already Installed**: `httpx` (backend), `recharts` (frontend)

**Files to Create**: `backend/routers/mandi.py`, `backend/services/mandi_service.py`, `backend/schemas/mandi.py`

**Files to Modify**: `backend/main.py` (register router), `frontend-next/src/app/market/page.tsx`

**API Key**: Already in `.env` — `DATA_GOV_API_KEY`

---

## Feature 2: "Should I Spray Today?" — Weather Spray Alerts

### Problem
The #1 cause of pesticide waste in Indian farming is spraying before unexpected rain. A farmer spends ₹500-2,000 on chemicals, sprays their field, and rain washes it off within hours. Open-Meteo gives free 7-day weather forecasts — nobody integrates it into a simple yes/no recommendation for spraying.

### What Changes
Add a dashboard widget and a dedicated `/weather` page. Shows today's spray recommendation as a prominent green checkmark (✅ Spray Today) or red X (❌ Wait — rain expected).

### Rules Engine
```
if rain_expected_within_6_hours:  ❌ WAIT — rain in X hours
if wind_speed > 15_kmh:           ❌ WAIT — wind will blow spray away
if temp > 35_celsius:             ❌ WAIT — chemicals evaporate too fast
if all_clear:                     ✅ GO — spray now, next rain in Y hours
```

### Technical Implementation

**Backend** — New file: `backend/routers/weather.py`

```
Endpoint: GET /weather/spray-advisory?lat=15.82&lon=78.03&crop=cotton
```

- Calls `https://api.open-meteo.com/v1/forecast?latitude=XX&longitude=YY&hourly=precipitation,wind_speed_10m,temperature_2m&forecast_days=2`
- Applies spray rules engine
- Returns: `{ can_spray: true/false, reason: "...", next_safe_window: "Today 2PM-5PM", next_rain: "Tomorrow 6AM", forecast: {hourly temps, rain, wind} }`

**Frontend** — New file: `frontend-next/src/app/weather/page.tsx`
- Prominent green/red indicator card at top
- Hourly breakdown table for next 24h
- 2-day forecast graph
- Dashboard widget: small card in `/` page showing today's status

**Dependencies**: None (Open-Meteo is a free GET API, no key needed)

**API Key**: `WEATHER_API_KEY=be6140aec55569abc2f9eda7462abda7` (OpenWeatherMap — if this ever activates, use it instead)

**Files to Create**: `backend/routers/weather.py`, `backend/services/weather_service.py`, `backend/schemas/weather.py`, `frontend-next/src/app/weather/page.tsx`

**Files to Modify**: `backend/main.py`, `frontend-next/src/app/page.tsx` (add dashboard widget)

---

## Feature 3: Government Scheme Eligibility Checker

### Problem
PM-KISAN gives ₹6,000/year to every eligible small farmer. PMFBY (crop insurance) covers crop losses. Kisan Credit Card gives low-interest loans. Soil Health Cards give free soil testing. Most eligible farmers don't apply because: (a) they don't know these schemes exist, (b) navigating 14 different government websites is impossible, (c) eligibility criteria are buried in PDFs.

### What Changes
New `/schemes` page. Farmer fills: state, district, land_size (acres), crop_type, annual_income (optional). The app shows every scheme they qualify for with: scheme name, benefit amount, apply link, and the documents they need to bring.

### Technical Implementation

**Backend** — New file: `backend/routers/schemes.py`

```
Endpoint: POST /schemes/check
Body: { state, district, land_size_acres, crop_type, annual_income? }
Response: { eligible: [{name, benefit, eligibility_reason, apply_url, documents_needed}] }
```

**Scheme Database** (static JSON, built-in):

| Scheme | Eligibility | Benefit | Apply Link |
|--------|------------|---------|------------|
| PM-KISAN | All small/marginal farmers (<2ha) | ₹6,000/year in 3 installments | pmkisan.gov.in |
| PMFBY | Insurable crops, before sowing | Full crop loss coverage, 2% premium | pmfby.gov.in |
| Kisan Credit Card | Active farmer, any land size | ₹1.6-3 lakh loan at 4% interest | Bank branch + Aadhaar |
| Soil Health Card | Any farmer, once per 3 years | Free soil test + fertilizer recommendation | soilhealth.dac.gov.in |
| PM-KUSUM | Has uncultivated land, groundwater | 60% subsidy on solar pump | pmkusum.mnre.gov.in |
| e-NAM | Any farmer selling notified crops | Direct mandi access, no middleman | enam.gov.in |
| RKVY | State-specific, varied criteria | Infrastructure + crop diversification grants | rkvy.nic.in |
| NADCP | Dairy/poultry/fisheries farmers | Subsidized livestock + training | dadf.gov.in |

- Logic: filter schemes by state eligibility, land size category, and crop type match
- Returns 3-8 matching schemes for a typical small farmer

**Frontend** — New file: `frontend-next/src/app/schemes/page.tsx`
- Simple form: state dropdown, district dropdown, land size slider, crop selector, income (optional)
- Results: card grid with scheme name, rupee benefit, green "You're Eligible" badge
- Each card has: "What You Get" (₹ amount), "Documents Needed" (Aadhaar, land record, bank passbook), "Apply Here" (external link)
- Bottom: "Show All Schemes" toggle for awareness

**Files to Create**: `backend/routers/schemes.py`, `backend/services/scheme_service.py`, `backend/schemas/schemes.py`, `frontend-next/src/app/schemes/page.tsx`

**Files to Modify**: `backend/main.py`

**Dependencies**: None (static data, no external API needed)

---

## Feature 5: Mandi Comparison — "Where Should I Sell?"

### Problem
Farmers typically sell at the nearest mandi. But the nearest mandi isn't always the best price. A tomato farmer in Kurnool might get ₹1,800/quintal locally but ₹2,080 in Nandyal — a ₹280 difference that covers transport and yields pure profit.

### What Changes
Extends the live mandi prices feature. After the farmer selects a crop, the app queries ALL mandis within a 100km radius and ranks them by price. Shows the price difference minus estimated transport cost.

### Technical Implementation

**Backend** — Add to `backend/routers/mandi.py`

```
Endpoint: GET /api/mandi/compare?crop=tomato&lat=15.82&lon=78.03&quantity_qtl=10
```

- Query data.gov.in for all mandis in the state for that crop
- Filter to mandis within 100km radius (haversine formula from lat/lon)
- Estimate transport cost: ₹15/km for pickup truck (realistic for Indian rural transport)
- Calculate net gain: (mandi_price × quantity) − transport_cost
- Rank by net gain descending
- Returns top 5 mandis with: mandi_name, price, distance, transport_cost, net_gain, recommendation

**Frontend** — Add to market page as a toggle: "Compare Mandis" button
- Shows a comparison table: Mandi | Price | Distance | Transport | Net Gain
- Highlights the best option in green
- "Sell at ___ mandi" call-to-action with share button (WhatsApp share the recommendation)

**Files to Modify**: `backend/routers/mandi.py`, `backend/services/mandi_service.py`, `frontend-next/src/app/market/page.tsx`

---

## Implementation Order (Build in This Sequence)

```
Day 1: Feature 1 (Live Mandi Prices) → Removes fake data, adds real value immediately
Day 2: Feature 2 (Weather Spray Alerts) → Adds dashboard widget + new page
Day 3: Feature 5 (Mandi Comparison) → Extends Feature 1, same API
Day 4: Feature 3 (Government Schemes) → Static data, no external dependencies
```

## New Pages to Add

| Page | Route | Navigation Label |
|------|-------|-----------------|
| Weather | `/weather` | ☁️ Weather |
| Schemes | `/schemes` | 🏛️ Govt Schemes |
| Mandi (updated) | `/market` | 📊 Mandi Prices |

## Sidebar Update

After adding weather + schemes:

1. 📊 Dashboard
2. 🛠️ Farm Tools
3. 🔬 Disease Scanner
4. 📈 Mandi Prices
5. ☁️ Weather
6. 🏛️ Govt Schemes
7. 🤖 Farm Assistant
8. 🧑‍🌾 Profile
9. 📝 Feedback
