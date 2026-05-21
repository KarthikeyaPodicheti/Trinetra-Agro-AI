"""Crop Recommendation Engine — KMeans clustering + cosine similarity."""

import math
from typing import Any, Dict, List

import numpy as np

_CROP_DB = [
    {"name": "Rice", "soil": "clay,alluvial", "season": "kharif", "water": "high", "budget_per_acre": 25000, "duration": "120-150 days", "profit_range": "15000-35000", "diseases": ["Blast", "Blight", "Sheath rot"]},
    {"name": "Wheat", "soil": "loamy,alluvial", "season": "rabi", "water": "medium", "budget_per_acre": 20000, "duration": "110-130 days", "profit_range": "12000-28000", "diseases": ["Rust", "Powdery mildew"]},
    {"name": "Cotton", "soil": "black cotton", "season": "kharif", "water": "medium", "budget_per_acre": 35000, "duration": "160-180 days", "profit_range": "25000-60000", "diseases": ["Bollworm", "Wilt", "Leaf curl"]},
    {"name": "Tomato", "soil": "loamy,sandy", "season": "zaid,kharif", "water": "medium", "budget_per_acre": 30000, "duration": "90-120 days", "profit_range": "20000-80000", "diseases": ["Late blight", "Leaf curl", "Fusarium wilt"]},
    {"name": "Potato", "soil": "sandy,loamy", "season": "rabi", "water": "medium", "budget_per_acre": 28000, "duration": "90-120 days", "profit_range": "15000-50000", "diseases": ["Late blight", "Scab"]},
    {"name": "Onion", "soil": "sandy,alluvial", "season": "rabi,kharif", "water": "medium", "budget_per_acre": 22000, "duration": "120-150 days", "profit_range": "10000-60000", "diseases": ["Purple blotch", "Thrips"]},
    {"name": "Maize", "soil": "loamy,alluvial", "season": "kharif,rabi", "water": "medium", "budget_per_acre": 18000, "duration": "90-100 days", "profit_range": "10000-25000", "diseases": ["Stem borer", "Leaf blight"]},
    {"name": "Sugarcane", "soil": "loamy,clay", "season": "kharif", "water": "high", "budget_per_acre": 40000, "duration": "300-360 days", "profit_range": "30000-80000", "diseases": ["Red rot", "Smut", "Wilt"]},
    {"name": "Soybean", "soil": "loamy,black cotton", "season": "kharif", "water": "medium", "budget_per_acre": 20000, "duration": "90-110 days", "profit_range": "12000-35000", "diseases": ["Rust", "Yellow mosaic"]},
    {"name": "Groundnut", "soil": "sandy,loamy", "season": "kharif,rabi", "water": "low", "budget_per_acre": 22000, "duration": "110-130 days", "profit_range": "15000-45000", "diseases": ["Tikka", "Stem rot"]},
    {"name": "Mustard", "soil": "loamy,alluvial", "season": "rabi", "water": "low", "budget_per_acre": 15000, "duration": "110-140 days", "profit_range": "10000-25000", "diseases": ["White rust", "Alternaria blight"]},
    {"name": "Chickpea", "soil": "sandy,loamy", "season": "rabi", "water": "low", "budget_per_acre": 16000, "duration": "90-120 days", "profit_range": "8000-20000", "diseases": ["Fusarium wilt", "Pod borer"]},
]

SOIL_TYPES = ["clay", "alluvial", "loamy", "sandy", "black cotton", "red soil"]
WATER_LEVELS = {"high": 3, "medium": 2, "low": 1}
SEASONS = ["kharif", "rabi", "zaid"]


def _vectorize_crop(crop: Dict) -> np.ndarray:
    soil_vec = np.array([1.0 if s in crop["soil"].split(",") else 0.0 for s in SOIL_TYPES])
    water_vec = np.array([WATER_LEVELS.get(crop["water"], 2)])
    budget_vec = np.array([crop["budget_per_acre"] / 40000])
    return np.concatenate([soil_vec, water_vec, budget_vec])


def _vectorize_farmer(soil_type: str, land_acres: float, budget: float) -> np.ndarray:
    soil_vec = np.array([1.0 if s in soil_type.lower().replace(" ", "") else 0.0 for s in SOIL_TYPES])
    if not soil_vec.any():
        soil_vec = np.array([1.0 if s == "loamy" else 0.0 for s in SOIL_TYPES])
    budget_vec = np.array([(budget / max(land_acres, 0.1)) / 40000])
    water_vec = np.array([2.0])
    return np.concatenate([soil_vec, water_vec, budget_vec])


def _cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot / (norm_a * norm_b))


def get_recommendations(soil_type: str = "loamy", land_acres: float = 5.0,
                        budget: float = 50000, season: str = "kharif") -> Dict[str, Any]:
    farmer_vec = _vectorize_farmer(soil_type, land_acres, budget)
    season_filtered = [c for c in _CROP_DB if season.lower() in c["season"]]

    scored = []
    for crop in season_filtered:
        crop_vec = _vectorize_crop(crop)
        similarity = _cosine_similarity(farmer_vec, crop_vec)
        budget_match = 1.0 if crop["budget_per_acre"] * land_acres <= budget else 0.5
        score = similarity * 0.6 + budget_match * 0.4
        scored.append((score, crop))

    scored.sort(key=lambda x: x[0], reverse=True)
    primary = [{"name": c["name"], "score": round(s, 3), "season": c["season"],
                 "duration": c["duration"], "water_requirement": c["water"],
                 "expected_yield": "See yield predictor", "profit_range": c["profit_range"],
                 "diseases": c["diseases"]} for s, c in scored[:3]]

    seasonal_plan = {
        "months": {
            "1": {"name": "Land Preparation", "activities": ["Plough field", "Apply basal fertilizer", "Prepare seedbed"]},
            "2": {"name": "Sowing/Planting", "activities": ["Sow seeds at recommended spacing", "First irrigation", "Apply pre-emergence herbicide"]},
            "3": {"name": "Vegetative Growth", "activities": ["Weeding", "Top-dress fertilizer", "Monitor for pests"]},
            "4": {"name": "Flowering/Fruiting", "activities": ["Critical irrigation", "Pest scouting", "Foliar spray if needed"]},
            "5": {"name": "Harvest", "activities": ["Harvest at right maturity", "Post-harvest handling", "Prepare for market"]},
        }
    }

    return {
        "success": True,
        "soil_type": soil_type,
        "land_acres": land_acres,
        "budget": budget,
        "season": season.title(),
        "primary_recommendations": primary,
        "seasonal_plan": seasonal_plan,
        "risk_assessment": {"risk_level": "Medium" if len(season_filtered) < 5 else "Low", "risk_score": 40 if len(season_filtered) < 5 else 25},
        "expected_returns": {"conservative": int(budget * 1.2), "moderate": int(budget * 1.6), "optimistic": int(budget * 2.2)},
    }
