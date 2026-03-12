"""
Trinetra Agro AI - Irrigation AI Module
Calculates daily/weekly water requirements and provides scheduling advice.
"""

from datetime import datetime
from typing import Dict, Any

# Water requirement data  (cm per crop season, and daily avg mm)
_WATER_DATA = {
    'rice':       {'season_cm': 175, 'daily_mm': 8.0,  'method': 'Flood / Puddled'},
    'wheat':      {'season_cm': 50,  'daily_mm': 3.5,  'method': 'Sprinkler / Furrow'},
    'cotton':     {'season_cm': 70,  'daily_mm': 4.5,  'method': 'Drip / Furrow'},
    'tomato':     {'season_cm': 70,  'daily_mm': 5.0,  'method': 'Drip'},
    'potato':     {'season_cm': 60,  'daily_mm': 4.0,  'method': 'Sprinkler / Drip'},
    'onion':      {'season_cm': 55,  'daily_mm': 3.5,  'method': 'Drip / Sprinkler'},
    'maize':      {'season_cm': 65,  'daily_mm': 4.5,  'method': 'Furrow / Sprinkler'},
    'sugarcane':  {'season_cm': 180, 'daily_mm': 6.0,  'method': 'Furrow / Drip'},
    'soybean':    {'season_cm': 50,  'daily_mm': 3.5,  'method': 'Sprinkler'},
    'groundnut':  {'season_cm': 55,  'daily_mm': 3.5,  'method': 'Sprinkler / Drip'},
}

# Growth stage water multipliers (fraction of peak demand)
_STAGE_MULT = {
    'Initial (0-20%)':    0.5,
    'Vegetative (20-50%)': 0.8,
    'Flowering (50-75%)':  1.0,
    'Maturity (75-100%)':  0.6,
}

# Season adjustment (summer needs more, monsoon less)
_SEASON_ADJ = {
    'kharif': 0.7,   # monsoon rains supplement
    'rabi':   1.0,
    'zaid':   1.3,    # hot summer
}


def _current_season() -> str:
    m = datetime.now().month
    if m in (6, 7, 8, 9, 10):
        return 'kharif'
    elif m in (11, 12, 1, 2, 3):
        return 'rabi'
    return 'zaid'


def irrigation_plan(crop: str, land_acres: float = 1.0,
                    growth_stage: str = "Vegetative (20-50%)") -> Dict[str, Any]:
    """
    Generate an irrigation plan for the given crop & land.

    Returns daily and weekly water needs (litres), recommended method,
    schedule, and water-saving tips.
    """
    key = crop.lower().strip()
    data = _WATER_DATA.get(key)
    if data is None:
        return {"success": False,
                "error": f"No irrigation data for '{crop}'. Supported: {list(_WATER_DATA)}"}

    season = _current_season()
    season_mult = _SEASON_ADJ.get(season, 1.0)
    stage_mult = _STAGE_MULT.get(growth_stage, 0.8)

    # 1 acre ≈ 4047 m²
    area_m2 = land_acres * 4047

    daily_mm = data['daily_mm'] * season_mult * stage_mult
    daily_litres = daily_mm * area_m2  # 1mm on 1m² = 1 litre
    weekly_litres = daily_litres * 7

    schedule = _schedule(key, daily_mm, season)

    return {
        "success": True,
        "crop": crop.title(),
        "land_acres": land_acres,
        "growth_stage": growth_stage,
        "season": season.title(),
        "recommended_method": data['method'],
        "water_needs": {
            "daily_mm": round(daily_mm, 1),
            "daily_litres": round(daily_litres),
            "weekly_litres": round(weekly_litres),
            "season_total_cm": data['season_cm'],
        },
        "schedule": schedule,
        "tips": _tips(key, season),
    }


def _schedule(crop, daily_mm, season):
    if daily_mm > 6:
        freq = "Daily"
        duration = "2-3 hours per session"
    elif daily_mm > 4:
        freq = "Every 2 days"
        duration = "1.5-2 hours per session"
    else:
        freq = "Every 3 days"
        duration = "1-1.5 hours per session"

    if season == 'kharif':
        rain_note = "Reduce frequency during active rainfall"
    else:
        rain_note = "Increase if temperatures exceed 35°C"

    return {
        "frequency": freq,
        "duration": duration,
        "best_time": "Early morning (6-8 AM) or late evening (5-7 PM)",
        "note": rain_note,
    }


def _tips(crop, season):
    tips = [
        "Use soil moisture sensors to avoid over-watering",
        "Apply mulch to reduce evaporation by 25-30%",
    ]
    if crop in ('tomato', 'cotton', 'onion', 'potato'):
        tips.append("Drip irrigation can save 30-50% water vs flood method")
    if crop == 'rice':
        tips.append("Alternate Wetting and Drying (AWD) saves 15-30% water in rice")
    if season == 'zaid':
        tips.append("Summer crops need more frequent, lighter irrigations")
    tips.append("Avoid irrigating during peak sun hours to minimize evaporation")
    return tips
