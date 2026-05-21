"""Pydantic schemas for authentication."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: Optional[str] = None
    phone: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenRefresh(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class FarmerProfileCreate(BaseModel):
    soil_type: Optional[str] = None
    land_size_acres: Optional[float] = Field(default=None, ge=0.1, le=500)
    budget_inr: Optional[float] = Field(default=None, ge=1000, le=10_000_000)
    location: Optional[str] = None
    crops: Optional[list[str]] = None
    irrigation_type: Optional[str] = None
    experience_years: Optional[int] = Field(default=None, ge=0)


class FarmerProfileResponse(FarmerProfileCreate):
    id: str
    user_id: str

    model_config = {"from_attributes": True}
