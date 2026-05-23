"""Risk Engine — multi-dimensional farm risk assessment."""

from typing import Any, Dict

CROP_RISK_PROFILES = {
    "rice": {"disease_risk": 60, "market_risk": 30, "water_risk": 70},
    "wheat": {"disease_risk": 40, "market_risk": 25, "water_risk": 30},
    "cotton": {"disease_risk": 65, "market_risk": 55, "water_risk": 40},
    "tomato": {"disease_risk": 70, "market_risk": 70, "water_risk": 50},
    "potato": {"disease_risk": 55, "market_risk": 50, "water_risk": 40},
    "onion": {"disease_risk": 45, "market_risk": 80, "water_risk": 35},
    "maize": {"disease_risk": 40, "market_risk": 35, "water_risk": 35},
    "sugarcane": {"disease_risk": 50, "market_risk": 20, "water_risk": 60},
    "soybean": {"disease_risk": 45, "market_risk": 40, "water_risk": 30},
    "groundnut": {"disease_risk": 35, "market_risk": 35, "water_risk": 25},
}


def assess_risk(crop: str, soil_type: str = "loamy", land_acres: float = 5.0,
                budget: float = 50000, irrigation: bool = True) -> Dict[str, Any]:
    key = crop.lower().strip()
    profile = CROP_RISK_PROFILES.get(key, {"disease_risk": 50, "market_risk": 50, "water_risk": 50})

    water_risk = profile["water_risk"] if not irrigation else max(10, profile["water_risk"] - 30)
    budget_per_acre = budget / max(land_acres, 0.1)
    budget_risk = max(10, min(90, 80 - int(budget_per_acre / 1000)))
    land_risk = min(80, int(land_acres * 3)) if land_acres > 10 else 20

    breakdown = {
        "disease_risk": profile["disease_risk"],
        "market_risk": profile["market_risk"],
        "water_risk": water_risk,
        "budget_risk": budget_risk,
        "land_risk": land_risk,
    }

    risk_score = sum(breakdown.values()) / len(breakdown)
    if risk_score < 35:
        risk_level = "Low"
    elif risk_score < 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "success": True,
        "crop": crop.title(),
        "risk_score": round(risk_score, 1),
        "risk_level": risk_level,
        "breakdown": breakdown,
        "mitigations": [
            "Use disease-resistant seed varieties",
            "Diversify crops to reduce market risk",
            "Install drip irrigation to reduce water risk",
        ],
    }
