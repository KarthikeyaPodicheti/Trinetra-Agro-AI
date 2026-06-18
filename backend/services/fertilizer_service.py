from typing import Dict, Any

# ICAR-based fertilizer recommendations per crop (kg/acre NPK at moderate yield)
FERTILIZER_DATA = {
    "Cotton": {"N": 20, "P": 13, "K": 17, "urea": 43, "dap": 28, "mop": 28, "cost": 1850,
        "schedule": [
            {"stage": "Basal (sowing)", "urea": 0, "dap": 28, "mop": 14, "note": "Full P + half K at sowing"},
            {"stage": "Square formation (45 DAS)", "urea": 22, "dap": 0, "mop": 0, "note": "First N top-dressing after thinning"},
            {"stage": "Flowering (70 DAS)", "urea": 21, "dap": 0, "mop": 14, "note": "Remaining N + K at peak boll stage"},
        ],
        "tip": "Apply gypsum 100 kg/acre for sulphur if soil test shows deficiency. Avoid excess N.",
        "subsidy": "Buy at cooperative society: urea ~Rs 266/bag (subsidised), DAP ~Rs 1,350/bag, MOP ~Rs 1,650/bag.",
    },
    "Rice": {"N": 26, "P": 13, "K": 13, "urea": 56, "dap": 28, "mop": 22, "cost": 2050,
        "schedule": [
            {"stage": "Basal (transplanting)", "urea": 0, "dap": 28, "mop": 11, "note": "Full P + half K at transplanting"},
            {"stage": "Active tillering (25 DAT)", "urea": 28, "dap": 0, "mop": 0, "note": "First N top-dressing"},
            {"stage": "Panicle initiation (50 DAT)", "urea": 28, "dap": 0, "mop": 11, "note": "Remaining N + K - CRITICAL stage"},
        ],
        "tip": "Apply ZnSO4 25 kg/acre if zinc deficiency visible. Split N into 2-3 doses for best efficiency.",
        "subsidy": "Cooperative rates: urea ~Rs 266/bag, DAP ~Rs 1,350/bag, MOP ~Rs 1,650/bag.",
    },
    "Wheat": {"N": 26, "P": 13, "K": 9, "urea": 56, "dap": 28, "mop": 15, "cost": 1900,
        "schedule": [
            {"stage": "Basal (sowing)", "urea": 0, "dap": 28, "mop": 15, "note": "Full P + full K at sowing"},
            {"stage": "Crown root (21 DAS)", "urea": 28, "dap": 0, "mop": 0, "note": "First N with first irrigation"},
            {"stage": "Jointing (55 DAS)", "urea": 28, "dap": 0, "mop": 0, "note": "Remaining N - crucial for tiller count"},
        ],
        "tip": "Apply 20 kg sulphur/acre if growing on sandy soils. Do NOT skip crown root irrigation.",
        "subsidy": "Cooperative rates: urea ~Rs 266/bag, DAP ~Rs 1,350/bag, MOP ~Rs 1,650/bag.",
    },
    "Maize": {"N": 26, "P": 17, "K": 9, "urea": 56, "dap": 37, "mop": 15, "cost": 2200,
        "schedule": [
            {"stage": "Basal (sowing)", "urea": 0, "dap": 37, "mop": 15, "note": "Full P + K at sowing"},
            {"stage": "Knee-high (25 DAS)", "urea": 28, "dap": 0, "mop": 0, "note": "First N top-dressing after thinning"},
            {"stage": "Tasseling (50 DAS)", "urea": 28, "dap": 0, "mop": 0, "note": "Remaining N - water stress = poor pollination"},
        ],
        "tip": "Maize is a heavy Zn feeder. Apply ZnSO4 20 kg/acre if soil Zn is low. Earthing up at 30-35 DAS prevents lodging.",
        "subsidy": "Cooperative rates: urea ~Rs 266/bag, DAP ~Rs 1,350/bag, MOP ~Rs 1,650/bag.",
    },
    "Soybean": {"N": 9, "P": 26, "K": 17, "urea": 20, "dap": 56, "mop": 28, "cost": 2300,
        "schedule": [
            {"stage": "Basal (sowing)", "urea": 0, "dap": 56, "mop": 14, "note": "Full P + half K. Inoculate with Rhizobium."},
            {"stage": "Vegetative (30 DAS)", "urea": 20, "dap": 0, "mop": 0, "note": "Starter N - only if nodules are poor"},
            {"stage": "Flowering (50 DAS)", "urea": 0, "dap": 0, "mop": 14, "note": "K for pod filling - critical stage"},
        ],
        "tip": "Soybean fixes its own nitrogen - do NOT over-apply urea. Apply sulphur 20 kg/acre. Rhizobium inoculation is more important than fertilizer.",
        "subsidy": "Cooperative rates: urea ~Rs 266/bag, DAP ~Rs 1,350/bag, MOP ~Rs 1,650/bag.",
    },
    "Groundnut": {"N": 4, "P": 17, "K": 13, "urea": 9, "dap": 37, "mop": 22, "cost": 1600,
        "schedule": [
            {"stage": "Basal (sowing)", "urea": 0, "dap": 37, "mop": 11, "note": "Full P + half K. Apply gypsum 200 kg/acre."},
            {"stage": "Pegging (35 DAS)", "urea": 9, "dap": 0, "mop": 0, "note": "Starter N + gypsum at pegging"},
            {"stage": "Pod development (55 DAS)", "urea": 0, "dap": 0, "mop": 11, "note": "K for kernel filling"},
        ],
        "tip": "Gypsum at pegging prevents empty pods (pops). Apply 200 kg/acre between rows at flowering.",
        "subsidy": "Cooperative rates: urea ~Rs 266/bag, DAP ~Rs 1,350/bag, MOP ~Rs 1,650/bag.",
    },
    "Sugarcane": {"N": 70, "P": 26, "K": 22, "urea": 152, "dap": 56, "mop": 37, "cost": 4800,
        "schedule": [
            {"stage": "Basal (planting)", "urea": 0, "dap": 56, "mop": 19, "note": "Full P + half K + ZnSO4 10 kg/acre"},
            {"stage": "Tillering (45 DAP)", "urea": 76, "dap": 0, "mop": 0, "note": "First N dose + earthing up"},
            {"stage": "Grand growth (90 DAP)", "urea": 76, "dap": 0, "mop": 18, "note": "Second N + remaining K - peak demand"},
        ],
        "tip": "Sugarcane consumes the most nutrients. Split urea into 3 doses for 12-month varieties. Apply micronutrient mixture (Fe+Zn+Mn) if leaves show interveinal chlorosis.",
        "subsidy": "Cooperative rates: urea ~Rs 266/bag, DAP ~Rs 1,350/bag, MOP ~Rs 1,650/bag.",
    },
}


def calculate_fertilizer(crop: str, soil: str = "alluvial", target_yield: str = "moderate") -> Dict[str, Any]:
    crop = crop.capitalize()
    if crop not in FERTILIZER_DATA:
        return {"error": f"No data for '{crop}'. Available: {', '.join(FERTILIZER_DATA.keys())}"}

    d = dict(FERTILIZER_DATA[crop])
    ym = {"moderate": 1.0, "good": 1.2, "maximum": 1.4}.get(target_yield.lower(), 1.0)

    if ym != 1.0:
        for k in ["N", "P", "K", "urea", "dap", "mop", "cost"]:
            d[k] = round(d[k] * ym)

    d["soil"] = soil
    d["target_yield"] = target_yield

    return d
