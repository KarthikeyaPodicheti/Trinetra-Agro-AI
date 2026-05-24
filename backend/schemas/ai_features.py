"""Pydantic schemas for AI feature requests/responses."""

from pydantic import BaseModel, Field


class MarketRequest(BaseModel):
    crop: str
    days: int = Field(default=14, ge=7, le=30)
    location: str = ""
