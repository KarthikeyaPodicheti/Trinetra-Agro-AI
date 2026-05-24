"""Market Forecasting Engine — real data from data.gov.in + trend analysis."""

import requests
from datetime import datetime, timedelta
from typing import Any, Dict, List

from backend.core.config import get_settings

RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
BASE_URL = "https://api.data.gov.in/resource"

# Fallback base prices if API fails
FALLBACK_PRICES = {
    'rice': 2200, 'wheat': 2150, 'cotton': 6500, 'tomato': 1800,
    'potato': 1500, 'onion': 2000, 'maize': 1900, 'sugarcane': 350,
    'soybean': 4500, 'groundnut': 5500,
}

SUPPORTED_CROPS = list(FALLBACK_PRICES.keys())


def _fetch_market_data(crop: str, api_key: str) -> List[Dict]:
    """Fetch real market prices from data.gov.in."""
    try:
        params = {
            "api-key": api_key,
            "format": "json",
            "filters[commodity]": crop.title(),
            "limit": 50,
            "sort[arrival_date]": "desc",
        }
        resp = requests.get(f"{BASE_URL}/{RESOURCE_ID}", params=params, timeout=15)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("records", [])
    except Exception:
        pass
    return []


def predict_prices(crop: str, days: int = 14, location: str = "") -> Dict[str, Any]:
    key = crop.lower().strip()
    if key not in FALLBACK_PRICES and key not in [c.lower() for c in SUPPORTED_CROPS]:
        return {"success": False, "error": f"No data for '{crop}'. Supported: {SUPPORTED_CROPS}"}

    settings = get_settings()
    api_key = settings.data_gov_api_key
    records = _fetch_market_data(crop, api_key) if api_key else []

    today = datetime.now()

    if records:
        # Use real data
        prices_data = []
        for r in records:
            try:
                modal_price = float(r.get("modal_price", 0))
                if modal_price > 0:
                    prices_data.append({
                        "price": modal_price,
                        "market": r.get("market", ""),
                        "state": r.get("state", ""),
                        "date": r.get("arrival_date", ""),
                        "min_price": float(r.get("min_price", 0)),
                        "max_price": float(r.get("max_price", 0)),
                    })
            except (ValueError, TypeError):
                continue

        if prices_data:
            current_price = round(prices_data[0]["price"])
            avg_price = round(sum(p["price"] for p in prices_data) / len(prices_data))
            min_price = round(min(p["min_price"] for p in prices_data if p["min_price"] > 0) if any(p["min_price"] > 0 for p in prices_data) else current_price * 0.8)
            max_price = round(max(p["max_price"] for p in prices_data))

            # Trend from recent data
            if len(prices_data) >= 3:
                recent_avg = sum(p["price"] for p in prices_data[:3]) / 3
                older_avg = sum(p["price"] for p in prices_data[-3:]) / 3
                trend_val = recent_avg - older_avg
            else:
                trend_val = 0

            if trend_val > current_price * 0.02:
                trend = "upward"
            elif trend_val < -current_price * 0.02:
                trend = "downward"
            else:
                trend = "stable"

            # Generate forecast based on trend
            forecast_prices = [current_price]
            daily_change = trend_val / max(len(prices_data), 1)
            for i in range(1, days):
                next_p = forecast_prices[-1] + daily_change + ((-1)**i * current_price * 0.005)
                forecast_prices.append(round(max(min_price * 0.9, min(max_price * 1.1, next_p))))

            if trend == "upward":
                action, message = "Hold", "Prices trending up — wait for peak before selling"
            elif trend == "downward":
                action, message = "Sell", "Prices declining — sell now to avoid further loss"
            else:
                action, message = "Monitor", "Stable market — no urgency to buy or sell"

            # Top markets
            markets = list({f"{p['market']}, {p['state']}" for p in prices_data[:10] if p['market']})[:5]

            return {
                "success": True,
                "crop": crop.title(),
                "location": location or "All India",
                "current_price": current_price,
                "avg_price": avg_price,
                "min_price": min_price,
                "max_price": max_price,
                "trend": trend,
                "confidence": "High",
                "predictions": {
                    "dates": [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)],
                    "prices": forecast_prices,
                    "moving_avg": forecast_prices,
                    "trend": [round(current_price + (daily_change * i)) for i in range(days)],
                },
                "recommendation": {"action": action, "message": message, "reason": f"Based on {len(prices_data)} real mandi records", "urgency": "medium" if trend != "stable" else "low"},
                "market_tips": [
                    f"Data from {len(prices_data)} mandi records",
                    f"Price range: ₹{min_price} - ₹{max_price}/quintal",
                    f"Average across mandis: ₹{avg_price}/quintal",
                ],
                "top_markets": markets,
                "data_source": {"current_price_source": "data.gov.in (real mandi data)", "current_price_updated_at": prices_data[0].get("date", today.isoformat()), "market_records_used": len(prices_data)},
            }

    # Fallback to synthetic if API fails
    import random
    base = FALLBACK_PRICES.get(key, 2000)
    rng = random.Random(hash(f"{key}{today.strftime('%Y%m%d')}"))
    prices = [base]
    for i in range(1, days):
        prices.append(round(max(base * 0.8, min(base * 1.2, prices[-1] + rng.uniform(-20, 20)))))

    trend_val = prices[-1] - prices[0]
    trend = "upward" if trend_val > base * 0.03 else "downward" if trend_val < -base * 0.03 else "stable"
    action = "Hold" if trend == "upward" else "Sell" if trend == "downward" else "Monitor"
    message = "Prices trending up" if trend == "upward" else "Prices declining" if trend == "downward" else "Stable market"

    return {
        "success": True,
        "crop": crop.title(),
        "location": location or "Local mandi",
        "current_price": prices[0],
        "trend": trend,
        "confidence": "Low",
        "predictions": {
            "dates": [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)],
            "prices": prices,
            "moving_avg": prices,
            "trend": prices,
        },
        "recommendation": {"action": action, "message": message, "reason": "Synthetic estimate (API unavailable)", "urgency": "low"},
        "market_tips": ["⚠️ Using estimated data — real mandi API unavailable", "Check local mandi for actual rates"],
        "data_source": {"current_price_source": "synthetic fallback", "current_price_updated_at": today.isoformat(), "market_records_used": 0},
    }
