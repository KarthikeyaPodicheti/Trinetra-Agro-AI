"""
Trinetra Agro AI - Profit Predictor Module
Combines yield estimation × market price − input costs → projected profit.
"""

from typing import Dict, Any

# Estimated input costs per acre (₹) — seeds, fertilizer, labour, pesticides, misc
_INPUT_COSTS = {
    'rice':       {'seeds': 3000, 'fertilizer': 5000, 'labour': 10000, 'pesticide': 3000, 'misc': 4000},
    'wheat':      {'seeds': 2500, 'fertilizer': 4000, 'labour': 8000,  'pesticide': 2000, 'misc': 3500},
    'cotton':     {'seeds': 4000, 'fertilizer': 6000, 'labour': 12000, 'pesticide': 5000, 'misc': 8000},
    'tomato':     {'seeds': 3500, 'fertilizer': 5000, 'labour': 12000, 'pesticide': 4000, 'misc': 5500},
    'potato':     {'seeds': 8000, 'fertilizer': 5000, 'labour': 10000, 'pesticide': 3000, 'misc': 2000},
    'onion':      {'seeds': 3000, 'fertilizer': 4000, 'labour': 9000,  'pesticide': 2000, 'misc': 4000},
    'maize':      {'seeds': 2000, 'fertilizer': 3500, 'labour': 7000,  'pesticide': 2000, 'misc': 3500},
    'sugarcane':  {'seeds': 6000, 'fertilizer': 7000, 'labour': 15000, 'pesticide': 4000, 'misc': 8000},
    'soybean':    {'seeds': 2500, 'fertilizer': 3000, 'labour': 7000,  'pesticide': 2000, 'misc': 5500},
    'groundnut':  {'seeds': 4000, 'fertilizer': 3500, 'labour': 8000,  'pesticide': 2000, 'misc': 4500},
}

# Approximate selling price per ton (₹) — conservative / moderate / optimistic
_PRICE_PER_TON = {
    'rice':       (18000, 22000, 28000),
    'wheat':      (18000, 21500, 26000),
    'cotton':     (50000, 55000, 65000),
    'tomato':     (8000,  18000, 30000),
    'potato':     (6000,  12000, 20000),
    'onion':      (8000,  15000, 28000),
    'maize':      (14000, 19000, 24000),
    'sugarcane':  (2800,  3500,  4200),
    'soybean':    (35000, 45000, 55000),
    'groundnut':  (40000, 50000, 60000),
}


def predict_profit(crop: str, land_acres: float = 1.0,
                   soil_type: str = "", irrigation: bool = True,
                   yield_tons: float = None) -> Dict[str, Any]:
    """
    Project profit / loss for growing *crop* on *land_acres*.

    If *yield_tons* is not given, uses the yield_prediction module.
    """
    key = crop.lower().strip()
    costs_data = _INPUT_COSTS.get(key)
    prices = _PRICE_PER_TON.get(key)
    if costs_data is None or prices is None:
        return {"success": False,
                "error": f"No data for '{crop}'. Supported: {list(_INPUT_COSTS)}"}

    # Total input cost
    total_cost_per_acre = sum(costs_data.values())
    total_cost = total_cost_per_acre * land_acres

    # Yield estimate
    if yield_tons is None:
        from .yield_prediction import predict_yield
        y = predict_yield(crop, land_acres, soil_type, irrigation)
        if not y.get("success"):
            return y
        yields = y["estimates"]
    else:
        yields = {
            "conservative": yield_tons * 0.7,
            "moderate": yield_tons,
            "optimistic": yield_tons * 1.2,
        }

    price_low, price_mid, price_high = prices

    # Revenue scenarios
    rev_con = yields["conservative"] * price_low
    rev_mod = yields["moderate"] * price_mid
    rev_opt = yields["optimistic"] * price_high

    profit_con = rev_con - total_cost
    profit_mod = rev_mod - total_cost
    profit_opt = rev_opt - total_cost

    return {
        "success": True,
        "crop": crop.title(),
        "land_acres": land_acres,
        "input_costs": {
            "per_acre": total_cost_per_acre,
            "total": round(total_cost),
            "breakdown": costs_data,
        },
        "yield_tons": {
            "conservative": round(yields["conservative"], 2),
            "moderate": round(yields["moderate"], 2),
            "optimistic": round(yields["optimistic"], 2),
        },
        "revenue": {
            "conservative": round(rev_con),
            "moderate": round(rev_mod),
            "optimistic": round(rev_opt),
        },
        "profit": {
            "conservative": round(profit_con),
            "moderate": round(profit_mod),
            "optimistic": round(profit_opt),
        },
        "roi_percent": {
            "conservative": round(profit_con / total_cost * 100, 1) if total_cost else 0,
            "moderate": round(profit_mod / total_cost * 100, 1) if total_cost else 0,
            "optimistic": round(profit_opt / total_cost * 100, 1) if total_cost else 0,
        },
        "recommendation": _recommendation(profit_mod, total_cost),
    }


def _recommendation(profit_mod, total_cost):
    roi = profit_mod / total_cost * 100 if total_cost else 0
    if roi > 80:
        return "Highly profitable — strong recommendation to grow this crop"
    elif roi > 40:
        return "Good profitability — recommended with proper management"
    elif roi > 0:
        return "Marginal profit — proceed with caution, optimise inputs"
    else:
        return "Potential loss — consider alternative crops or reducing costs"
