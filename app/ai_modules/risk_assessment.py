"""
Trinetra Agro AI - Risk Assessment Module
Evaluates farming risks across weather, disease, market, and water dimensions.
"""

from datetime import datetime
from typing import Dict, Any


# Disease risk by crop (probability 0-1)
_DISEASE_RISK = {
    'rice': 0.6, 'wheat': 0.4, 'cotton': 0.7, 'tomato': 0.8,
    'potato': 0.6, 'onion': 0.5, 'maize': 0.5, 'sugarcane': 0.5,
    'soybean': 0.4, 'groundnut': 0.4,
}

# Market volatility score (0-1, higher = riskier)
_MARKET_VOLATILITY = {
    'rice': 0.2, 'wheat': 0.2, 'cotton': 0.7, 'tomato': 0.9,
    'potato': 0.5, 'onion': 0.9, 'maize': 0.4, 'sugarcane': 0.2,
    'soybean': 0.5, 'groundnut': 0.4,
}

# Water-intensity rating (0-1, higher = more water needed)
_WATER_NEED = {
    'rice': 0.9, 'wheat': 0.4, 'cotton': 0.5, 'tomato': 0.5,
    'potato': 0.5, 'onion': 0.4, 'maize': 0.5, 'sugarcane': 0.9,
    'soybean': 0.4, 'groundnut': 0.4,
}


def assess_risk(crop: str, soil_type: str = "", land_size: float = 1.0,
                budget: float = 50000, irrigation: bool = True) -> Dict[str, Any]:
    """
    Return a comprehensive risk assessment dict.

    Risk score 0-100.  Levels: Low (<30), Medium (30-60), High (>60).
    """
    crop_key = crop.lower().strip()
    score = 0.0
    factors = []

    # 1. Disease risk (0-30 pts)
    disease_prob = _DISEASE_RISK.get(crop_key, 0.5)
    disease_pts = disease_prob * 30
    score += disease_pts
    if disease_prob >= 0.6:
        factors.append(f"{crop.title()} is prone to multiple diseases (risk {disease_prob*100:.0f}%)")

    # 2. Market volatility (0-25 pts)
    vol = _MARKET_VOLATILITY.get(crop_key, 0.5)
    market_pts = vol * 25
    score += market_pts
    if vol >= 0.7:
        factors.append(f"Market prices for {crop.title()} are highly volatile")

    # 3. Water / irrigation risk (0-25 pts)
    water_need = _WATER_NEED.get(crop_key, 0.5)
    if not irrigation:
        water_pts = water_need * 25
        factors.append("No irrigation — rain dependency increases risk")
    else:
        water_pts = water_need * 10  # irrigation reduces risk
    score += water_pts

    # 4. Budget adequacy (0-10 pts)
    min_budget_per_acre = {
        'rice': 25000, 'wheat': 20000, 'cotton': 35000, 'tomato': 30000,
        'potato': 28000, 'onion': 22000, 'maize': 18000, 'sugarcane': 40000,
        'soybean': 20000, 'groundnut': 22000,
    }
    needed = min_budget_per_acre.get(crop_key, 25000) * land_size
    if budget < needed:
        gap_pct = min(1.0, (needed - budget) / needed)
        score += gap_pct * 10
        factors.append(f"Budget (₹{budget:,.0f}) is below estimated need (₹{needed:,.0f})")

    # 5. Small farm penalty (0-10 pts)
    if land_size < 2:
        score += 10
        factors.append("Small land holding limits economies of scale")

    score = min(score, 100)
    level = "Low" if score < 30 else ("Medium" if score < 60 else "High")

    mitigations = _mitigations(factors)

    return {
        "crop": crop.title(),
        "risk_score": round(score, 1),
        "risk_level": level,
        "factors": factors,
        "mitigations": mitigations,
        "breakdown": {
            "disease_risk": round(disease_pts, 1),
            "market_risk": round(market_pts, 1),
            "water_risk": round(water_pts, 1),
        },
    }


def _mitigations(factors):
    tips = []
    for f in factors:
        fl = f.lower()
        if "disease" in fl:
            tips.append("Use disease-resistant crop varieties")
            tips.append("Follow Integrated Pest Management (IPM) practices")
        if "volatile" in fl or "market" in fl:
            tips.append("Diversify crops to spread market risk")
            tips.append("Consider contract farming or forward selling")
        if "irrigation" in fl or "rain" in fl:
            tips.append("Invest in drip/sprinkler irrigation")
            tips.append("Mulch to conserve soil moisture")
        if "budget" in fl:
            tips.append("Explore government subsidies (PM-KISAN, RKVY)")
            tips.append("Start with lower-investment crops first")
        if "small" in fl:
            tips.append("Join a Farmer Producer Organization (FPO)")
    return list(dict.fromkeys(tips))  # deduplicate preserving order
