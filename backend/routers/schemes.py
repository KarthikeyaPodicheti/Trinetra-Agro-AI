"""Government schemes router."""

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Optional

from backend.schemas.schemes import SchemeResponse
from backend.services.scheme_service import check_eligibility

router = APIRouter(prefix="/schemes", tags=["schemes"])


class SchemeCheckRequest(BaseModel):
    state: str = Field(..., description="State name e.g. Maharashtra, Andhra Pradesh")
    land_size_acres: float = Field(..., ge=0.1, description="Land size in acres")
    crop_type: str = Field(default="", description="Main crop being grown")
    annual_income: Optional[float] = Field(default=None, description="Annual income in ₹")
    farmer_category: str = Field(default="all", description="all / dairy_poultry")


@router.post("/check", response_model=SchemeResponse)
async def check_schemes(data: SchemeCheckRequest):
    result = check_eligibility(
        state=data.state,
        land_size_acres=data.land_size_acres,
        crop_type=data.crop_type,
        annual_income=data.annual_income,
        farmer_category=data.farmer_category,
    )
    return SchemeResponse(**result)
