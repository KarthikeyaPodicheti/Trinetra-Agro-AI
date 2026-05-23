"""Irrigation AI Engine — water requirement planning."""

from typing import Any, Dict

CROP_WATER_DATA = {
    "rice": {"daily_mm": 8, "method": "Flood/Paddy irrigation", "frequency": "Daily"},
    "wheat": {"daily_mm": 4, "method": "Sprinkler or border irrigation", "frequency": "Every 7-10 days"},
    "cotton": {"daily_mm": 5, "method": "Drip irrigation", "frequency": "Every 5-7 days"},
    "tomato": {"daily_mm": 5, "method": "Drip irrigation", "frequency": "Every 3-4 days"},
    "potato": {"daily_mm": 5, "method": "Sprinkler irrigation", "frequency": "Every 5-7 days"},
    "onion": {"daily_mm": 4, "method": "Drip irrigation", "frequency": "Every 4-5 days"},
    "maize": {"daily_mm": 5, "method": "Furrow irrigation", "frequency": "Every 7-10 days"},
    "sugarcane": {"daily_mm": 7, "method": "Furrow irrigation", "frequency": "Every 7 days"},
    "soybean": {"daily_mm": 4, "method": "Sprinkler irrigation", "frequency": "Every 7-10 days"},
    "groundnut": {"daily_mm": 4, "method": "Sprinkler irrigation", "frequency": "Every 10 days"},
}

SUPPORTED_CROPS = list(CROP_WATER_DATA.keys())

GROWTH_STAGE_MULTIPLIER = {
    "Seedling (0-20%)": 0.6,
    "Vegetative (20-50%)": 1.0,
    "Flowering (50-75%)": 1.2,
    "Maturity (75-100%)": 0.7,
}


def irrigation_plan(crop: str, land_acres: float = 1.0,
                    growth_stage: str = "Vegetative (20-50%)") -> Dict[str, Any]:
    key = crop.lower().strip()
    if key not in CROP_WATER_DATA:
        return {"success": False, "error": f"Unsupported crop '{crop}'. Supported: {SUPPORTED_CROPS}"}

    data = CROP_WATER_DATA[key]
    multiplier = GROWTH_STAGE_MULTIPLIER.get(growth_stage, 1.0)
    daily_litres = data["daily_mm"] * land_acres * 4047 / 1000 * multiplier  # mm * m2 -> litres

    return {
        "success": True,
        "crop": crop.title(),
        "land_acres": land_acres,
        "growth_stage": growth_stage,
        "water_needs": {
            "daily_litres": round(daily_litres),
            "weekly_litres": round(daily_litres * 7),
            "daily_mm": round(data["daily_mm"] * multiplier, 1),
        },
        "method": data["method"],
        "frequency": data["frequency"],
        "schedule": [
            {"time": "6:00 AM", "duration_min": 30, "note": "Morning irrigation preferred"},
            {"time": "5:00 PM", "duration_min": 20, "note": "Evening top-up if needed"},
        ],
        "tips": [
            "Avoid irrigation during peak sun (11AM-3PM)",
            "Check soil moisture before irrigating",
            f"Drip irrigation saves 30-50% water for {crop.title()}",
        ],
    }
