"""Profit Engine — cost/revenue/ROI estimation per crop."""

from typing import Any, Dict

CROP_ECONOMICS = {
    "rice": {"cost_per_acre": 25000, "yield_kg": 2500, "price_per_kg": 22},
    "wheat": {"cost_per_acre": 20000, "yield_kg": 2000, "price_per_kg": 22},
    "cotton": {"cost_per_acre": 35000, "yield_kg": 800, "price_per_kg": 65},
    "tomato": {"cost_per_acre": 30000, "yield_kg": 15000, "price_per_kg": 18},
    "potato": {"cost_per_acre": 28000, "yield_kg": 10000, "price_per_kg": 15},
    "onion": {"cost_per_acre": 22000, "yield_kg": 8000, "price_per_kg": 20},
    "maize": {"cost_per_acre": 18000, "yield_kg": 2500, "price_per_kg": 19},
    "sugarcane": {"cost_per_acre": 40000, "yield_kg": 30000, "price_per_kg": 3.5},
    "soybean": {"cost_per_acre": 20000, "yield_kg": 1000, "price_per_kg": 45},
    "groundnut": {"cost_per_acre": 22000, "yield_kg": 1200, "price_per_kg": 55},
}

SUPPORTED_CROPS = list(CROP_ECONOMICS.keys())


def predict_profit(crop: str, land_acres: float = 1.0,
                   irrigation: bool = True) -> Dict[str, Any]:
    key = crop.lower().strip()
    if key not in CROP_ECONOMICS:
        return {"success": False, "error": f"Unsupported crop '{crop}'. Supported: {SUPPORTED_CROPS}"}

    data = CROP_ECONOMICS[key]
    cost = data["cost_per_acre"] * land_acres
    revenue = data["yield_kg"] * land_acres * data["price_per_kg"]
    if not irrigation:
        revenue *= 0.7  # 30% yield reduction without irrigation

    profit = revenue - cost
    roi = (profit / cost) * 100 if cost > 0 else 0

    return {
        "success": True,
        "crop": crop.title(),
        "land_acres": land_acres,
        "cost_total": round(cost),
        "revenue": round(revenue),
        "profit": round(profit),
        "roi_percent": round(roi, 1),
        "cost_breakdown": {
            "seeds": round(cost * 0.15),
            "fertilizer": round(cost * 0.25),
            "labour": round(cost * 0.30),
            "irrigation": round(cost * 0.15),
            "pesticides": round(cost * 0.10),
            "misc": round(cost * 0.05),
        },
    }
