from datetime import date, timedelta
from typing import List, Dict, Any, Optional


# Stage-wise crop calendar data from ICAR / agriculture university recommendations
# Each stage: week_offset (from sowing), name, advisory (irrigation, fertilizer, pest, general)

CROP_CALENDARS: Dict[str, List[Dict[str, Any]]] = {
    "Cotton": [
        {"week": 0, "stage": "Sowing", "irrigation": "Light pre-sowing irrigation only", "fertilizer": "Apply 50% N + full P & K as basal dose (20:60:40 NPK kg/acre)", "pest": "Treat seeds with Imidacloprid 5g/kg before sowing", "tip": "Sow at 90×60 cm spacing. Use Bt cotton seeds if available."},
        {"week": 1, "stage": "Germination", "irrigation": "No irrigation needed — soil moisture sufficient", "fertilizer": "None", "pest": "Watch for cutworms at seedling base", "tip": "Gap-fill missing plants within 10 days"},
        {"week": 3, "stage": "Seedling Growth", "irrigation": "First light irrigation if no rain for 10+ days", "fertilizer": "Apply remaining 50% N as top dressing after thinning", "pest": "Check leaf undersides for aphids. Spray Neem oil 5ml/L if found.", "tip": "Remove weeds between rows — first weeding due now"},
        {"week": 5, "stage": "Vegetative Growth", "irrigation": "Irrigate once every 10-12 days (furrow method)", "fertilizer": "Foliar spray: MgSO4 5g/L for magnesium", "pest": "Install pheromone traps for bollworm monitoring (4-5 per acre)", "tip": "Pinch terminal bud at 60-70 days for bushy growth"},
        {"week": 7, "stage": "Square Formation", "irrigation": "Critical stage — do NOT skip irrigation. Water stress now = flower drop", "fertilizer": "Foliar spray: DAP 2% for better square retention", "pest": "Spray Chlorantraniliprole 0.4ml/L for bollworm if trap count >8 moths/week", "tip": "Second weeding due. Mulch between rows to retain moisture."},
        {"week": 9, "stage": "Flowering", "irrigation": "Irrigate every 7-8 days. Avoid waterlogging.", "fertilizer": "Apply KNO3 3g/L foliar spray for boll size", "pest": "⚠️ Peak bollworm risk. Scout 20 plants daily at random. Spray only if 5% damage seen.", "tip": "White flowers appear — avoid pesticide during daytime (kills pollinators)"},
        {"week": 11, "stage": "Boll Development", "irrigation": "Reduce to once every 12-15 days", "fertilizer": "None", "pest": "Monitor for pink bollworm inside bolls. Apply ETL-based spray only.", "tip": "Bolls will start opening in 2-3 weeks"},
        {"week": 13, "stage": "Boll Opening", "irrigation": "Stop irrigation completely", "fertilizer": "None", "pest": "Watch for mealybugs on open bolls", "tip": "First picking begins. Pick only fully open, dry bolls for best quality."},
        {"week": 15, "stage": "Harvest", "irrigation": "None", "fertilizer": "None", "pest": "Remove and destroy crop residue after harvest to break pest cycle", "tip": "Pick in morning hours when dew is gone. Store in dry place away from moisture."},
    ],
    "Rice": [
        {"week": 0, "stage": "Nursery / Transplanting", "irrigation": "Maintain 2-3 cm standing water in field", "fertilizer": "Apply 60:30:30 NPK as basal (40% N + full P & K)", "pest": "Dip roots in Chlorpyriphos solution before transplanting", "tip": "Transplant 25-30 day old seedlings at 20×15 cm spacing"},
        {"week": 2, "stage": "Tillering", "irrigation": "Maintain 5 cm water level. Do not let field dry.", "fertilizer": "Apply 30% N at active tillering (20-25 days after transplanting)", "pest": "Watch for stem borer — dead hearts at tiller base. Apply Cartap HCl 1.5 kg/acre if 5% affected.", "tip": "Mild water stress at this stage actually promotes root growth"},
        {"week": 4, "stage": "Maximum Tillering", "irrigation": "Maintain 5 cm water. Occasional drainage (2 days) improves soil aeration.", "fertilizer": "Apply remaining 30% N at panicle initiation", "pest": "Leaf folder — look for rolled leaves. Spray only if 10% leaves affected.", "tip": "Golden rule: alternate wetting and drying saves 30% water without yield loss"},
        {"week": 6, "stage": "Panicle Initiation", "irrigation": "⚠️ Most water-sensitive stage. Do NOT let field dry. Maintain 5 cm water.", "fertilizer": "Apply ZnSO4 25 kg/acre if zinc deficiency (yellow leaves) visible", "pest": "Brown planthopper — check stem base for insects. Apply Buprofezin 25SC if found.", "tip": "This is the make-or-break stage for yield. Water stress = empty grains."},
        {"week": 8, "stage": "Flowering / Grain Filling", "irrigation": "Maintain 4-5 cm water. Drain 7 days before harvest.", "fertilizer": "Foliar spray: KCl 1% for grain weight improvement", "pest": "Rice earhead bug — check 10 random panicles. Spray only if >5 bugs/panicle.", "tip": "Grain filling takes 25-30 days. Weather at this stage determines quality."},
        {"week": 11, "stage": "Ripening & Harvest", "irrigation": "Drain field completely 7-10 days before harvest", "fertilizer": "None", "pest": "Rats — use community-level bait stations before harvest", "tip": "Harvest when 80% grains are golden yellow. Moisture content should be ~20%."},
    ],
    "Wheat": [
        {"week": 0, "stage": "Sowing", "irrigation": "Pre-sowing irrigation if soil moisture is low (preserves germination)", "fertilizer": "Apply 60:30:20 NPK as basal (full P & K + 50% N)", "pest": "Treat seeds with Carboxin 2g/kg for loose smut prevention", "tip": "Sow at 22.5 cm row spacing, 5 cm depth. Best time: 15-25 November."},
        {"week": 2, "stage": "Germination & Crown Root", "irrigation": "First irrigation (crown root stage) at 20-25 days after sowing", "fertilizer": "None — basal nutrients are sufficient", "pest": "Watch for termites in sandy soils. Apply Chlorpyriphos dust if visible.", "tip": "This is the most critical irrigation. Missing it reduces tillers by 40%."},
        {"week": 4, "stage": "Tillering", "irrigation": "Second irrigation at 40-45 days (tillering stage)", "fertilizer": "Apply remaining 50% N as top dressing after first irrigation", "pest": "Monitor for aphids on young leaves. Spray Neem oil at 5 ml/L if found.", "tip": "More tillers = more ears = more yield. Nitrogen now is crucial."},
        {"week": 6, "stage": "Jointing", "irrigation": "Third irrigation at 60-65 days (jointing/late tillering)", "fertilizer": "None", "pest": "Check for rust disease — orange pustules on leaves. Apply Propiconazole if >5% area affected.", "tip": "Stem elongation happening now. Lodging risk if nitrogen was excessive."},
        {"week": 8, "stage": "Booting & Heading", "irrigation": "Fourth irrigation at 80-85 days (booting/flowering). Do NOT skip.", "fertilizer": "Foliar spray: KNO3 2% for grain filling", "pest": "Armyworm — check leaf margins for chewing. Use Chlorantraniliprole if >2 larvae/m².", "tip": "Water stress now = shriveled grains at harvest."},
        {"week": 10, "stage": "Flowering & Grain Filling", "irrigation": "Fifth irrigation at 100 days (grain filling, if needed). Light irrigation only.", "fertilizer": "None", "pest": "Birds — use reflective tape / scare method if flock feeding", "tip": "Grains harden during this phase. Avoid waterlogging."},
        {"week": 13, "stage": "Ripening & Harvest", "irrigation": "Stop irrigation 10-12 days before harvest", "fertilizer": "None", "pest": "Rodent control — bait stations around field perimeter", "tip": "Harvest when grain moisture is 12-14%. Thresh immediately, dry to 10% for storage."},
    ],
    "Maize": [
        {"week": 0, "stage": "Sowing", "irrigation": "Pre-sowing irrigation for good germination", "fertilizer": "Apply 60:40:20 NPK as basal at sowing", "pest": "Seed treatment with Thiamethoxam 4g/kg for shoot fly protection", "tip": "Sow at 60×20 cm spacing for grain maize. Kharif: June-July, Rabi: Oct-Nov."},
        {"week": 2, "stage": "Seedling / Knee-high", "irrigation": "Light irrigation if no rain. Avoid waterlogging.", "fertilizer": "Apply 40% N as top dressing (20-25 days after sowing)", "pest": "Shoot fly — look for dead hearts in young plants. Apply Carbofuran granules if >2% affected.", "tip": "Thin to 1 plant per hill. Gap-fill where germination failed."},
        {"week": 4, "stage": "Vegetative Growth", "irrigation": "Irrigate every 10-12 days if dry spell", "fertilizer": "Apply remaining N (40%) at knee-high stage", "pest": "Stem borer — small holes in stem, sawdust-like frass. Apply Cartap HCl granules in whorl at 10 kg/ha.", "tip": "Earthing up (pulling soil around plant base) prevents lodging"},
        {"week": 6, "stage": "Tasseling", "irrigation": "⚠️ Most critical stage. Irrigate immediately if tassels emerging. Water stress = poor pollination.", "fertilizer": "None", "pest": "Fall armyworm — look for ragged leaf feeding, frass in whorl. Spray Spinetoram 0.3 ml/L if >10% whorls infested.", "tip": "Tassels produce pollen. Wind pollinates maize — plant in blocks, not single rows."},
        {"week": 8, "stage": "Silking & Grain Fill", "irrigation": "Light irrigation. Do not water-stress during grain fill.", "fertilizer": "Foliar spray: Urea 2% + ZnSO4 0.5% at silking for grain weight", "pest": "Cob borer — larvae enter silks. Apply Carbaryl 10% dust on silks if >5% cobs infested.", "tip": "Each silk thread connects to one kernel. Poor pollination = missing kernels on cob."},
        {"week": 10, "stage": "Dough Stage", "irrigation": "Reduce irrigation. Stop 10-15 days before harvest.", "fertilizer": "None", "pest": "Monitor for birds near maturity. Community-level bird scaring is most effective.", "tip": "Harvest when husk turns brown and dry. Grain moisture should be 20-25%."},
    ],
    "Soybean": [
        {"week": 0, "stage": "Sowing", "irrigation": "Sow in moist soil. Do not irrigate immediately after sowing.", "fertilizer": "Apply 20:60:40 NPK as basal. Inoculate seeds with Rhizobium culture before sowing.", "pest": "Mix Thiamethoxam-treated seed with Trichoderma for soil-borne disease prevention", "tip": "Sow at 45×5 cm spacing. Kharif: June 15-July 15 is ideal in most zones."},
        {"week": 2, "stage": "Seedling & Nodulation", "irrigation": "No irrigation needed unless extended dry spell (>12 days no rain)", "fertilizer": "None — Rhizobium fixes nitrogen at roots", "pest": "Girdle beetle — notches on stem. Spray Quinalphos 2 ml/L if >2 beetles/meter row.", "tip": "Check root nodules — healthy plants have 15-20 pinkish nodules on taproot."},
        {"week": 4, "stage": "Vegetative Growth", "irrigation": "First irrigation at 30-35 days if dry. Irrigate in furrows, not flood.", "fertilizer": "Apply Sulphur 20 kg/acre (Soybean is a heavy sulphur feeder)", "pest": "Leaf miner — serpentine mines on leaves. Spray Neem oil 5 ml/L + sticker if >5 leaves/plant affected.", "tip": "Weed-free period of first 30-45 days is critical. First weeding due now."},
        {"week": 6, "stage": "Flowering", "irrigation": "⚠️ Critical stage. Irrigate even if mild soil moisture deficit. 5 cm water depth via furrow.", "fertilizer": "Foliar spray: DAP 2% at 50% flowering for better pod set", "pest": "Tobacco caterpillar — look for skeletonized leaves in patches. Apply NPV virus 250 LE/acre at early instar stage.", "tip": "Flowers appear at nodes. Each node can produce 3-5 pods if conditions are right."},
        {"week": 8, "stage": "Pod Development", "irrigation": "Second irrigation if dry. Avoid heavy irrigation — pod rot risk in waterlogged soil.", "fertilizer": "None. Excessive nitrogen now reduces oil content in seeds.", "pest": "Pod borer — check for entry holes on developing pods. Apply Indoxacarb 0.5 ml/L if >3% pods infested.", "tip": "Pod filling takes 35-45 days. Weather determines seed size."},
        {"week": 10, "stage": "Maturity & Harvest", "irrigation": "Stop irrigation completely. Allow soil to dry.", "fertilizer": "None", "pest": "Store in dry, pest-free godown. Fumigate with Aluminium Phosphide if storing >3 months.", "tip": "Harvest when 95% pods turn brown and leaves drop. Thresh at 15% moisture. Dry to 10% for storage."},
    ],
    "Groundnut": [
        {"week": 0, "stage": "Sowing", "irrigation": "Sow in well-drained sandy loam. Light pre-sowing irrigation if needed.", "fertilizer": "Apply 10:40:20 NPK + Gypsum 200 kg/acre at sowing", "pest": "Seed treatment: Mancozeb 3g/kg + Chlorpyriphos 2ml/kg", "tip": "Sow at 30×10 cm spacing. Remove hard seed coat if using bold-seeded varieties."},
        {"week": 3, "stage": "Pegging", "irrigation": "⚠️ Critical stage. Irrigate to field capacity. Pegs enter soil now — dry soil = no pods.", "fertilizer": "Apply Gypsum 200 kg/acre at pegging (top dressing for calcium)", "pest": "Leaf miner — characteristic mines. Spray Quinalphos if >5 mines/leaf.", "tip": "Gypsum at pegging is the #1 groundnut hack — prevents 'pops' (empty pods)"},
        {"week": 6, "stage": "Pod Development", "irrigation": "Light irrigation every 12-15 days. Avoid water stagnation.", "fertilizer": "Foliar spray: Boron 0.1% for better kernel development", "pest": "White grub — wilting plants, chewed roots. Apply Phorate granules to soil if severity observed.", "tip": "Pods develop underground. Soil should be moist but not wet."},
        {"week": 9, "stage": "Harvest", "irrigation": "Stop irrigation 10-15 days before harvest", "fertilizer": "None", "pest": "Aflatoxin risk if dried improperly. Strip pods and sun-dry to 8-10% moisture within 3 days.", "tip": "Harvest indicator: inner shell turns dark. Pull a sample plant — 70-80% mature pods is right time."},
    ],
    "Sugarcane": [
        {"week": 0, "stage": "Planting", "irrigation": "Pre-planting irrigation. Plant setts in moist furrows.", "fertilizer": "Apply 50:60:40 NPK as basal + 10 kg Zinc sulphate/acre", "pest": "Dip setts in Carbendazim 1g/L for 15 min before planting", "tip": "Use 3-bud setts, 35,000-40,000 setts per acre. Plant at 90 cm row spacing."},
        {"week": 4, "stage": "Tillering", "irrigation": "Maintain field capacity. Furrow irrigation every 10-12 days.", "fertilizer": "First top dressing: 80 kg Urea/acre at 45 days", "pest": "Early shoot borer — dead hearts at 1-3 month stage. Apply Chlorantraniliprole granules.", "tip": "Earthing up + weeding due at 60-75 days"},
        {"week": 8, "stage": "Grand Growth", "irrigation": "⚠️ Rapid growth stage. Irrigate every 8-10 days. This is when cane puts on bulk.", "fertilizer": "Second top dressing: 80 kg Urea + 50 kg MOP/acre at 90 days", "pest": "Top borer — look for bunchy top. Apply Cartap HCl granules in whorl if >5% shoots affected.", "tip": "Peak water demand: sugarcane drinks 1,800-2,200 mm total in its lifecycle. This is the thirstiest phase."},
        {"week": 14, "stage": "Maturity / Ripening", "irrigation": "Reduce to every 15-20 days. Stop 3-4 weeks before harvest.", "fertilizer": "None — excess nitrogen now reduces sugar content", "pest": "Rat damage near harvest — set up community baiting", "tip": "Check maturity: use hand refractometer. Harvest when brix reading >18% (lower 1/3 of cane)"},
    ],
}


def generate_calendar(
    crop: str,
    sowing_date: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a week-by-week crop calendar starting from the sowing date.
    
    Args:
        crop: Crop name (case-sensitive, must match CROP_CALENDARS key)
        sowing_date: ISO date string (YYYY-MM-DD). Defaults to today.
    
    Returns:
        Dict with crop name, sowing_date, total_weeks, and timeline (list of week entries)
    """
    if crop not in CROP_CALENDARS:
        return {"error": f"No calendar data for '{crop}'. Available crops: {', '.join(CROP_CALENDARS.keys())}"}

    stages = CROP_CALENDARS[crop]

    if sowing_date:
        base_date = date.fromisoformat(sowing_date)
    else:
        base_date = date.today()

    timeline = []
    for s in stages:
        week_start = base_date + timedelta(weeks=s["week"])
        week_end = week_start + timedelta(days=6)
        timeline.append({
            "week_number": s["week"],
            "stage": s["stage"],
            "date_range": {
                "start": week_start.isoformat(),
                "end": week_end.isoformat(),
            },
            "irrigation": s["irrigation"],
            "fertilizer": s["fertilizer"],
            "pest_management": s["pest"],
            "tip": s["tip"],
        })

    total_days = (stages[-1]["week"]) * 7
    harvest_date = base_date + timedelta(days=total_days)

    return {
        "crop": crop,
        "sowing_date": base_date.isoformat(),
        "expected_harvest": harvest_date.isoformat(),
        "total_weeks": len(timeline),
        "timeline": timeline,
    }
