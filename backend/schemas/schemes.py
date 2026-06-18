"""Government schemes schemas."""

from typing import List, Optional
from pydantic import BaseModel


class SchemeItem(BaseModel):
    name: str
    full_name: str
    benefit: str
    description: str
    eligibility_reason: str
    apply_url: str
    documents: List[str]
    helpline: str


class FarmerProfile(BaseModel):
    state: str
    land_acres: float
    land_hectares: float
    crop: str = ""
    income: Optional[float] = None


class SchemeResponse(BaseModel):
    total_schemes: int
    eligible_count: int
    eligible: List[SchemeItem]
    profile: FarmerProfile
