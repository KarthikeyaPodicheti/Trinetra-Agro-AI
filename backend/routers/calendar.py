from fastapi import APIRouter, Query
from backend.services.crop_calendar_service import generate_calendar, CROP_CALENDARS

router = APIRouter(prefix="/calendar", tags=["Crop Calendar"])

@router.get("/generate")
async def get_crop_calendar(
    crop: str = Query(..., description="Crop name e.g. Cotton, Rice, Wheat, Maize, Soybean, Groundnut, Sugarcane"),
    sowing_date: str = Query(None, description="ISO date (YYYY-MM-DD). Defaults to today."),
):
    """Generate a week-by-week crop calendar from sowing to harvest."""
    return generate_calendar(crop, sowing_date)

@router.get("/crops")
async def list_crops():
    """List all crops with calendar data available."""
    return {"crops": list(CROP_CALENDARS.keys())}
