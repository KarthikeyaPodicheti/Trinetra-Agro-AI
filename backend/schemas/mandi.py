"""Mandi Price schemas."""

from pydantic import BaseModel, Field
from typing import Optional, List


class MandiPriceItem(BaseModel):
    mandi: str
    crop: str
    price_per_quintal: float
    state: str
    district: str
    date: str


class Recommendation(BaseModel):
    action: str  # hold, sell_now, monitor, no_data
    message: str


class MandiResponse(BaseModel):
    success: bool
    prices: List[MandiPriceItem] = []
    total_records: int = 0
    trend: str = "stable"
    recommendation: Optional[Recommendation] = None
    error: Optional[str] = None
