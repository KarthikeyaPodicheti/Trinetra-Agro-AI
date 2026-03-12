"""
Trinetra Agro AI - Yield Prediction Module
Statistical yield estimator based on crop database, soil, season, irrigation.
"""

from datetime import datetime
from typing import Dict, Any

# Expected yields (tons/hectare) — [min, max]
_YIELD_DATA = {
    'rice':       {'min': 3.0,  'max': 6.0,  'unit': 'tons/ha'},
    'wheat':      {'min': 3.0,  'max': 5.0,  'unit': 'tons/ha'},
    'cotton':     {'min': 1.5,  'max': 3.0,  'unit': 'tons/ha'},
    'tomato':     {'min': 40.0, 'max': 60.0, 'unit': 'tons/ha'},
    'potato':     {'min': 20.0, 'max': 30.0, 'unit': 'tons/ha'},
    'onion':      {'min': 20.0, 'max': 30.0, 'unit': 'tons/ha'},
    'maize':      {'min': 6.0,  'max': 10.0, 'unit': 'tons/ha'},
    'sugarcane':  {'min': 60.0, 'max': 80.0, 'unit': 'tons/ha'},
    'soybean':    {'min': 2.0,  'max': 3.0,  'unit': 'tons/ha'},
    'groundnut':  {'min': 2.0,  'max': 3.0,  'unit': 'tons/ha'},
}

# Soil suitability multiplier
_SOIL_MATCH = {
    'rice':      ['alluvial', 'clay', 'loamy'],
    'wheat':     ['alluvial', 'loamy', 'clay'],
    'cotton':    ['black cotton', 'clayey', 'loamy'],
    'tomato':    ['loamy', 'sandy loam'],
    'potato':    ['sandy loam', 'loamy'],
    'onion':     ['sandy loam', 'loamy'],
    'maize':     ['loamy', 'sandy loam'],
    'sugarcane': ['alluvial', 'loamy', 'black cotton'],
    'soybean':   ['sandy loam', 'loamy'],
    'groundnut': ['sandy loam', 'loamy'],
}

# Season suitability (primary seasons)
_SEASON_MATCH = {
    'rice': ['kharif'],
    'wheat': ['rabi'],
    'cotton': ['kharif'],
    'tomato': ['rabi', 'kharif'],
    'potato': ['rabi'],
    'onion': ['rabi', 'kharif'],
    'maize': ['kharif', 'rabi'],
    'sugarcane': ['kharif'],
    'soybean': ['kharif'],
    'groundnut': ['kharif', 'rabi'],
}


def _current_season() -> str:
    month = datetime.now().month
    if month in (6, 7, 8, 9, 10):
        return 'kharif'
    elif month in (11, 12, 1, 2, 3):
        return 'rabi'
    return 'zaid'


def predict_yield(crop: str, land_acres: float = 1.0,
                  soil_type: str = "", irrigation: bool = True) -> Dict[str, Any]:
    """
    Estimate yield for *crop* on *land_acres* acres.

    Returns conservative / moderate / optimistic estimates.
    """
    key = crop.lower().strip()
    data = _YIELD_DATA.get(key)
    if data is None:
        return {"success": False,
                "error": f"No yield data for '{crop}'. Supported: {list(_YIELD_DATA)}"}

    base_min = data['min']
    base_max = data['max']

    # 1 hectare ≈ 2.47 acres
    hectares = land_acres / 2.47

    # --- multipliers ---
    soil_mult = 1.0
    soil_norm = soil_type.lower().strip()
    ideal_soils = _SOIL_MATCH.get(key, [])
    if soil_norm and ideal_soils:
        if any(s in soil_norm for s in ideal_soils):
            soil_mult = 1.0
        else:
            soil_mult = 0.75  # sub-optimal soil

    season = _current_season()
    season_mult = 1.0
    if season not in _SEASON_MATCH.get(key, []):
        season_mult = 0.8  # off-season penalty

    irrig_mult = 1.0 if irrigation else 0.7

    overall = soil_mult * season_mult * irrig_mult

    est_min = base_min * overall * hectares
    est_max = base_max * overall * hectares
    est_mid = (est_min + est_max) / 2

    return {
        "success": True,
        "crop": crop.title(),
        "land_acres": land_acres,
        "land_hectares": round(hectares, 2),
        "unit": data['unit'].split('/')[0],  # e.g. "tons"
        "estimates": {
            "conservative": round(est_min, 2),
            "moderate": round(est_mid, 2),
            "optimistic": round(est_max, 2),
        },
        "multipliers": {
            "soil": soil_mult,
            "season": season_mult,
            "irrigation": irrig_mult,
        },
        "current_season": season.title(),
        "notes": _notes(key, soil_mult, season_mult, irrig_mult),
    }


def _notes(crop, soil_m, season_m, irrig_m):
    notes = []
    if soil_m < 1.0:
        notes.append("Soil type is not ideal — consider soil amendments")
    if season_m < 1.0:
        notes.append("Current season is off-peak for this crop")
    if irrig_m < 1.0:
        notes.append("Lack of irrigation significantly reduces yield")
    if not notes:
        notes.append("Conditions are favorable for good yield")
    return notes
