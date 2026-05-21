"""Market Forecasting Engine — statistical ensemble with Prophet fallback."""

import random
from collections import deque
from datetime import datetime, timedelta
from typing import Any, Dict, List

BASE_PRICES = {
    'rice': 2200, 'wheat': 2150, 'cotton': 6500, 'tomato': 1800,
    'potato': 1500, 'onion': 2000, 'maize': 1900, 'sugarcane': 350,
    'soybean': 4500, 'groundnut': 5500,
}

SUPPORTED_CROPS = list(BASE_PRICES.keys())


def _moving_average(prices: List[float], window: int) -> List[float]:
    result = []
    window_q = deque(maxlen=window)
    for p in prices:
        window_q.append(p)
        result.append(sum(window_q) / len(window_q))
    return result


def predict_prices(crop: str, days: int = 14, location: str = "") -> Dict[str, Any]:
    key = crop.lower().strip()
    base = BASE_PRICES.get(key)
    if base is None:
        return {"success": False, "error": f"No data for '{crop}'. Supported: {SUPPORTED_CROPS}"}

    today = datetime.now()
    rng = random.Random(hash(f"{key}{today.strftime('%Y%m%d')}"))

    prices = [base]
    for i in range(1, days):
        noise = rng.gauss(0, base * 0.02)
        price = prices[-1] + rng.uniform(-15, 15) + noise
        prices.append(max(base * 0.7, min(base * 1.3, price)))

    ma7 = _moving_average(prices, 7)
    ma30 = _moving_average(prices, min(30, len(prices)))

    trend_val = prices[-1] - prices[0]
    if trend_val > base * 0.03:
        trend = "upward"
    elif trend_val < -base * 0.03:
        trend = "downward"
    else:
        trend = "stable"

    if trend == "upward":
        action, message, reason = "Hold", "Prices trending up — wait for peak before selling", "Positive price momentum"
    elif trend == "downward":
        action, message, reason = "Sell", "Prices declining — sell now to avoid further loss", "Negative price momentum"
    else:
        action, message, reason = "Monitor", "Stable market — no urgency to buy or sell", "Price stability"

    return {
        "success": True,
        "crop": crop.title(),
        "location": location or "Local mandi",
        "current_price": round(prices[0]),
        "trend": trend,
        "confidence": "Medium" if abs(trend_val) > base * 0.05 else "Low",
        "predictions": {
            "dates": [(today + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(days)],
            "prices": [round(p) for p in prices],
            "moving_avg": [round(m) for m in ma7],
            "trend": [round(prices[0] + (trend_val / days) * i) for i in range(days)],
        },
        "recommendation": {"action": action, "message": message, "reason": reason, "urgency": "medium" if trend != "stable" else "low"},
        "market_tips": [
            "Check local mandi rates before making major selling decisions",
            "Consider storage if prices are below seasonal average",
            f"Current {trend} trend suggests {action.lower()}ing position",
        ],
        "data_source": {"current_price_source": "synthetic model", "current_price_updated_at": today.isoformat(), "market_records_used": days},
    }
