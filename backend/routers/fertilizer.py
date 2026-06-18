from fastapi import APIRouter, Query
from backend.services.fertilizer_service import calculate_fertilizer

router = APIRouter(prefix="/fertilizer", tags=["Fertilizer Calculator"])

@router.get("/calculate")
async def get_fertilizer(
    crop: str = Query(..., description="Crop name"),
    soil: str = Query("alluvial", description="Soil type"),
    target_yield: str = Query("moderate", description="moderate / good / maximum"),
):
    return calculate_fertilizer(crop, soil, target_yield)
