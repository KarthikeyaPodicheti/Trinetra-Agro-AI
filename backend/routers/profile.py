"""Farmer profile router — GET/PUT /profile."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_current_user, get_db
from backend.models import User, Farmer
from backend.schemas.auth import FarmerProfileCreate, FarmerProfileResponse

router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("", response_model=FarmerProfileResponse | None)
async def get_profile(user: User = Depends(get_current_user)):
    if user.farmer:
        return user.farmer
    return None


@router.put("", response_model=FarmerProfileResponse)
@router.post("", response_model=FarmerProfileResponse)
async def save_profile(data: FarmerProfileCreate, db: AsyncSession = Depends(get_db),
                       user: User = Depends(get_current_user)):
    if user.farmer:
        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(user.farmer, k, v)
    else:
        farmer = Farmer(user_id=user.id, **data.model_dump(exclude_unset=True))
        db.add(farmer)
    await db.flush()
    await db.refresh(user, ["farmer"])
    return user.farmer
