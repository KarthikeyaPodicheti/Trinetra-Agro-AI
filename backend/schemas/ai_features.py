"""Pydantic schemas for AI feature requests/responses."""

from typing import Optional

from pydantic import BaseModel, Field


class MarketRequest(BaseModel):
    crop: str
    days: int = Field(default=14, ge=7, le=30)
    location: str = ""


class AdvisorRequest(BaseModel):
    soil_type: str = "loamy"
    land_acres: float = Field(default=5.0, ge=0.1, le=500.0)
    budget: float = Field(default=50000, ge=1000, le=10_000_000)
    season: str = "kharif"


class IrrigationRequest(BaseModel):
    crop: str
    land_acres: float = Field(default=1.0, ge=0.1, le=500.0)
    growth_stage: str = "Vegetative (20-50%)"


class ProfitRequest(BaseModel):
    crop: str
    land_acres: float = Field(default=1.0, ge=0.1, le=500.0)
    irrigation: bool = True


class RiskRequest(BaseModel):
    crop: str
    soil_type: str = "loamy"
    land_acres: float = Field(default=5.0, ge=0.1, le=500.0)
    budget: float = Field(default=50000, ge=1000, le=10_000_000)
    irrigation: bool = True


class YieldRequest(BaseModel):
    crop: str
    land_acres: float = Field(default=1.0, ge=0.1, le=500.0)
    soil_type: str = "loamy"
    irrigation: bool = True
