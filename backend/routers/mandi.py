"""Mandi prices router — real-time crop prices from data.gov.in."""

from fastapi import APIRouter, Query
from typing import Optional

from backend.core.config import get_settings
from backend.schemas.mandi import MandiResponse
from backend.services.mandi_service import fetch_mandi_prices, COMMON_CROPS

router = APIRouter(prefix="/mandi", tags=["mandi"])

settings = get_settings()


@router.get("/prices", response_model=MandiResponse)
async def get_prices(
    crop: str = Query(..., description="Crop name e.g. Tomato, Onion, Rice"),
    state: Optional[str] = Query(None, description="State name"),
    district: Optional[str] = Query(None, description="District name"),
    limit: int = Query(30, ge=1, le=100),
):
    result = await fetch_mandi_prices(
        crop=crop,
        state=state,
        district=district,
        api_key=settings.data_gov_api_key,
        limit=limit,
    )
    return MandiResponse(**result)


@router.get("/crops")
async def list_crops():
    """Return list of common crops for autocomplete."""
    return {"crops": COMMON_CROPS}
