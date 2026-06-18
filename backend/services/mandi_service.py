"""Mandi price service — fetch live prices from data.gov.in API with caching."""

import asyncio
import time
from typing import Any, Dict, List, Optional

import httpx

DATA_GOV_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"

# Simple in-memory cache — keyed by (crop, state), 30-minute TTL
_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = 1800  # 30 minutes
_last_cleanup = time.time()

# Common Indian crops
COMMON_CROPS = [
    "Onion", "Tomato", "Potato", "Rice", "Wheat", "Maize", "Cotton",
    "Soybean", "Groundnut", "Sugarcane", "Banana", "Mango", "Brinjal",
    "Cabbage", "Cauliflower", "Peas", "Garlic", "Ginger", "Turmeric",
    "Chilli", "Coriander", "Cumin", "Mustard", "Sunflower", "Arhar/Tur",
    "Bengal Gram", "Black Gram", "Green Gram", "Jowar", "Bajra", "Ragi",
]

async def fetch_mandi_prices(crop: str, state: Optional[str] = None,
                              district: Optional[str] = None,
                              api_key: Optional[str] = None,
                              limit: int = 30) -> Dict[str, Any]:
    """Query data.gov.in mandi price API with caching. Returns structured results."""
    global _cache, _last_cleanup

    if api_key is None:
        from backend.core.config import get_settings
        api_key = get_settings().data_gov_api_key

    if not api_key:
        return {"success": False, "error": "DATA_GOV_API_KEY not configured", "prices": []}

    # Check cache
    cache_key = f"{crop.lower()}:{state or ''}"
    now = time.time()
    if now - _last_cleanup > 600:
        _cache.clear()
        _last_cleanup = now
    cached = _cache.get(cache_key)
    if cached and (now - cached["ts"]) < CACHE_TTL:
        return cached["data"]

    # Fetch from API with longer timeout
    params: Dict[str, Any] = {
        "api-key": api_key,
        "format": "json",
        "limit": min(limit, 50),
        "filters[commodity]": crop,
    }
    if state:
        params["filters[state]"] = state
    if district:
        params["filters[district]"] = district

    try:
        async with httpx.AsyncClient(timeout=45) as client:
            resp = await client.get(DATA_GOV_URL, params=params)
            if resp.status_code != 200:
                return {"success": False, "error": f"API returned {resp.status_code}", "prices": []}

            data = resp.json()
            records = data.get("records", [])
    except Exception as e:
        # Return stale cache if available
        if cached:
            return cached["data"]
        return {"success": False, "error": f"Government API unavailable: {e}", "prices": []}

    prices = _parse_records(records, crop)
    trend = _calculate_trend(prices)
    recommendation = _generate_recommendation(trend, prices)

    result = {
        "success": True,
        "prices": prices[:limit],
        "total_records": len(records),
        "trend": trend,
        "recommendation": recommendation,
    }

    # Store in cache
    _cache[cache_key] = {"ts": now, "data": result}
    return result


def _parse_records(records: List[Dict], crop: str) -> List[Dict]:
    prices = []
    for r in records:
        try:
            price = float(r.get("modal_price", 0))
        except (ValueError, TypeError):
            price = 0
        if price <= 0:
            continue
        prices.append({
            "mandi": r.get("market", "Unknown"),
            "crop": r.get("commodity", crop),
            "price_per_quintal": price,
            "state": r.get("state", ""),
            "district": r.get("district", ""),
            "date": r.get("arrival_date", ""),
        })
    prices.sort(key=lambda p: p["date"], reverse=True)
    return prices


def _calculate_trend(prices: List[Dict]) -> str:
    """Determine price trend from recent data."""
    if len(prices) < 3:
        return "stable"
    recent = [p["price_per_quintal"] for p in prices[:7]]
    if len(recent) < 3:
        return "stable"
    # Simple slope: first vs last 3 averages
    first_3 = sum(recent[-3:]) / 3
    last_3 = sum(recent[:3]) / 3
    change_pct = ((last_3 - first_3) / first_3) * 100 if first_3 > 0 else 0
    if change_pct > 5:
        return "rising"
    elif change_pct < -5:
        return "falling"
    return "stable"


def _generate_recommendation(trend: str, prices: List[Dict]) -> Dict[str, str]:
    """Generate buy/sell/hold suggestion."""
    if not prices:
        return {"action": "no_data", "message": "Not enough data for recommendation"}
    current = prices[0]["price_per_quintal"] if prices else 0
    avg = sum(p["price_per_quintal"] for p in prices[:7]) / min(len(prices), 7) if prices else current

    if trend == "rising":
        return {
            "action": "hold",
            "message": f"Prices are rising — consider waiting before selling. Current: ₹{current:.0f}/quintal",
        }
    elif trend == "falling":
        return {
            "action": "sell_now",
            "message": f"Prices are falling — sell now at ₹{current:.0f}/quintal to avoid further decline.",
        }
    else:
        dir_str = "above" if current > avg else "near"
        return {
            "action": "monitor",
            "message": f"Prices are stable {dir_str} average — monitor this week. Current: ₹{current:.0f}/quintal",
        }
