"""AI Feature Routers — market forecasting."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db, get_optional_user
from backend.models import User
from backend.schemas.ai_features import MarketRequest
from backend.services.ai_service import run_market

router = APIRouter(prefix="/ai", tags=["ai-features"])


@router.post("/market")
async def market_forecast(req: MarketRequest, db: AsyncSession = Depends(get_db),
                          user: Optional[User] = Depends(get_optional_user)):
    return await run_market(db, req, user)
