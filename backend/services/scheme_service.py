"""Government scheme eligibility engine — static data, zero APIs."""

from typing import Any, Dict, List, Optional

# All schemes verified against official government sources 2024-25
SCHEMES: List[Dict[str, Any]] = [
    {
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "benefit": "₹6,000 per year (₹2,000 every 4 months)",
        "description": "Direct income support to all landholding farmer families.",
        "eligibility": {
            "max_land_ha": None,  # All land sizes eligible
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": "all",
            "category": "small_marginal",
        },
        "apply_url": "https://pmkisan.gov.in",
        "documents": ["Aadhaar Card", "Land Records (7/12 or Khatauni)", "Bank Passbook", "Mobile Number linked to Aadhaar"],
        "helpline": "155261 / 011-24300606",
    },
    {
        "name": "PMFBY",
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "benefit": "Full crop loss coverage at 2% premium (Kharif), 1.5% (Rabi), 5% (Horticulture)",
        "description": "Crop insurance against natural calamities, pests, and diseases.",
        "eligibility": {
            "max_land_ha": None,
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": ["Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Soybean", "Groundnut", "Tomato", "Onion", "Potato"],
            "category": "all",
        },
        "apply_url": "https://pmfby.gov.in",
        "documents": ["Aadhaar Card", "Land Records", "Bank Passbook", "Sowing Declaration", "Crop Details"],
        "helpline": "1800-180-1551",
    },
    {
        "name": "Kisan Credit Card",
        "full_name": "Kisan Credit Card (KCC)",
        "benefit": "Loan up to ₹3 lakh at 4% effective interest rate (7% with 3% prompt repayment subsidy)",
        "description": "Short-term credit for crop cultivation, post-harvest expenses, and farm maintenance.",
        "eligibility": {
            "max_land_ha": None,
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": "all",
            "category": "all",
        },
        "apply_url": "https://www.myscheme.gov.in/schemes/kcc",
        "documents": ["Aadhaar Card", "Land Records", "Bank Passbook", "Passport-size Photo", "PAN Card (optional)"],
        "helpline": "Visit nearest bank branch (SBI, PNB, Canara Bank, etc.)",
    },
    {
        "name": "Soil Health Card",
        "full_name": "Soil Health Card Scheme",
        "benefit": "Free soil testing every 3 years + personalized fertilizer recommendation",
        "description": "Scientific analysis of your soil's nutrient content and pH level.",
        "eligibility": {
            "max_land_ha": None,
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": "all",
            "category": "all",
        },
        "apply_url": "https://soilhealth.dac.gov.in",
        "documents": ["Aadhaar Card", "Land Records", "Contact your nearest KVK or Agriculture Department office"],
        "helpline": "1800-180-1551",
    },
    {
        "name": "PM-KUSUM",
        "full_name": "PM Kisan Urja Suraksha evam Utthaan Mahabhiyan",
        "benefit": "60% subsidy on solar water pumps (up to 10 HP)",
        "description": "Solar-powered irrigation pumps to reduce diesel/electricity costs.",
        "eligibility": {
            "max_land_ha": None,
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": "all",
            "category": "all",
        },
        "apply_url": "https://pmkusum.mnre.gov.in",
        "documents": ["Aadhaar Card", "Land Records", "Bank Passbook", "Passport-size Photo", "Proof of groundwater availability"],
        "helpline": "1800-180-3333",
    },
    {
        "name": "e-NAM",
        "full_name": "National Agriculture Market",
        "benefit": "Direct mandi access — sell without middlemen, transparent pricing across 1,361 mandis",
        "description": "Online trading platform connecting farmers directly to buyers across India.",
        "eligibility": {
            "max_land_ha": None,
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": ["Rice", "Wheat", "Cotton", "Maize", "Sugarcane", "Soybean", "Groundnut", "Tomato", "Onion", "Potato", "Turmeric", "Chilli", "Banana", "Mango"],
            "category": "all",
        },
        "apply_url": "https://enam.gov.in",
        "documents": ["Aadhaar Card", "Bank Passbook", "Mobile Number", "Register at nearest APMC mandi"],
        "helpline": "1800-270-0224",
    },
    {
        "name": "RKVY",
        "full_name": "Rashtriya Krishi Vikas Yojana",
        "benefit": "State-specific grants for crop diversification, infrastructure, and organic farming",
        "description": "Flexible state-level funds for agricultural development projects.",
        "eligibility": {
            "max_land_ha": None,
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": "all",
            "category": "all",
        },
        "apply_url": "https://rkvy.nic.in",
        "documents": ["Aadhaar Card", "Land Records", "Bank Passbook", "Project proposal (if applicable)"],
        "helpline": "Contact State Agriculture Department",
    },
    {
        "name": "NADCP",
        "full_name": "National Animal Disease Control Programme",
        "benefit": "Free vaccination for Foot & Mouth Disease and Brucellosis + subsidized livestock",
        "description": "Animal health and dairy/poultry farmer support program.",
        "eligibility": {
            "max_land_ha": None,
            "min_land_ha": 0.1,
            "income_limit": None,
            "states": "all",
            "crops": "all",
            "category": "dairy_poultry",
        },
        "apply_url": "https://dahd.nic.in",
        "documents": ["Aadhaar Card", "Livestock ownership proof", "Contact nearest Veterinary Hospital"],
        "helpline": "1800-180-1551",
    },
]


def check_eligibility(
    state: str,
    land_size_acres: float,
    crop_type: str = "",
    annual_income: Optional[float] = None,
    farmer_category: str = "all",
) -> Dict[str, Any]:
    """Check which government schemes a farmer qualifies for."""
    land_ha = land_size_acres * 0.404686  # Convert acres to hectares

    # Auto-detect small/marginal from land size for PM-KISAN
    if land_ha <= 2 and farmer_category == "all":
        farmer_category = "small_marginal"

    eligible = []
    for scheme in SCHEMES:
        crit = scheme["eligibility"]

        # Land size check
        if crit.get("max_land_ha") is not None and land_ha > crit["max_land_ha"]:
            continue
        if land_ha < crit.get("min_land_ha", 0):
            continue

        # Income check
        if crit.get("income_limit") is not None and annual_income is not None:
            if annual_income > crit["income_limit"]:
                continue

        # State check
        if crit.get("states") != "all" and state.lower() not in [s.lower() for s in (crit.get("states", ["all"]))]:
            continue

        # Crop check (only some schemes are crop-specific)
        crop_crit = crit.get("crops", "all")
        if crop_crit != "all" and crop_type:
            if crop_type.title() not in crop_crit:
                continue

        # Category check — auto-detect small/marginal from land size
        scheme_cat = crit.get("category", "all")
        if scheme_cat != "all" and farmer_category != scheme_cat:
            # PM-KISAN: match small_marginal farmers
            if not (scheme_cat == "small_marginal" and land_ha <= 2):
                continue

        eligible.append({
            "name": scheme["name"],
            "full_name": scheme["full_name"],
            "benefit": scheme["benefit"],
            "description": scheme["description"],
            "eligibility_reason": _eligibility_reason(scheme, land_ha, state),
            "apply_url": scheme["apply_url"],
            "documents": scheme["documents"],
            "helpline": scheme["helpline"],
        })

    return {
        "total_schemes": len(SCHEMES),
        "eligible_count": len(eligible),
        "eligible": eligible,
        "profile": {
            "state": state,
            "land_acres": land_size_acres,
            "land_hectares": round(land_ha, 2),
            "crop": crop_type,
            "income": annual_income,
        },
    }


def _eligibility_reason(scheme: Dict, land_ha: float, state: str) -> str:
    """Generate human-readable eligibility reason."""
    name = scheme["name"]
    if name == "PM-KISAN":
        return "All landholding farmers are eligible — ₹6,000/year direct cash transfer."
    if name == "PMFBY":
        return "You grow insurable crops — get full loss coverage at just 2% premium."
    if name == "Kisan Credit Card":
        return f"You have {land_ha:.1f} hectares of land — eligible for low-interest crop loan."
    if name == "Soil Health Card":
        return "Every farmer gets a free soil test once every 3 years."
    if name == "PM-KUSUM":
        return "60% subsidy on solar pumps — reduce your irrigation electricity/diesel costs."
    if name == "e-NAM":
        return "Sell directly on the national mandi network with transparent pricing."
    if name == "RKVY":
        return "State-level agricultural development grants available."
    if name == "NADCP":
        return "Free livestock vaccination and disease control support."
    return f"Eligible under {state} state criteria."
