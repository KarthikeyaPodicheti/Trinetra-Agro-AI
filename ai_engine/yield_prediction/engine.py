"""Yield Prediction Engine — soil/irrigation-adjusted crop yield estimates."""

from typing import Any, Dict

BASE_YIELDS = {
    "rice": 2500, "wheat": 2000, "cotton": 800, "tomato": 15000,
    "potato": 10000, "onion": 8000, "maize": 2500, "sugarcane": 30000,
    "soybean": 1000, "groundnut": 1200,
}

SUPPORTED_CROPS = list(BASE_YIELDS.keys())

SOIL_MULTIPLIERS = {
    "alluvial": 1.2, "loamy": 1.1, "clay": 1.0, "black cotton": 1.05,
    "sandy": 0.8, "red soil": 0.85, "laterite": 0.75,
}


def predict_yield(crop: str, land_acres: float = 1.0,
                  soil_type: str = "loamy", irrigation: bool = True) -> Dict[str, Any]:
    key = crop.lower().strip()
    if key not in BASE_YIELDS:
        return {"success": False, "error": f"Unsupported crop '{crop}'. Supported: {SUPPORTED_CROPS}"}

    base = BASE_YIELDS[key]
    soil_mult = SOIL_MULTIPLIERS.get(soil_type.lower().strip(), 0.9)
    irrig_mult = 1.0 if irrigation else 0.65

    moderate = base * land_acres * soil_mult * irrig_mult
    conservative = moderate * 0.75
    optimistic = moderate * 1.25

    return {
        "success": True,
        "crop": crop.title(),
        "land_acres": land_acres,
        "soil_type": soil_type,
        "irrigation": irrigation,
        "estimates": {
            "conservative": round(conservative),
            "moderate": round(moderate),
            "optimistic": round(optimistic),
        },
        "unit": "kg",
        "multipliers": {"soil": soil_mult, "irrigation": irrig_mult},
    }
