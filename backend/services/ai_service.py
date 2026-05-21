"""AI Service — market forecasting and crop advisor with DB persistence."""

from typing import Any, Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ai_engine.market_forecasting.engine import predict_prices as _market
from ai_engine.recommendation_engine.engine import get_recommendations as _advisor
from backend.models import MarketPrediction, User
from backend.schemas.ai_features import AdvisorRequest, MarketRequest


async def run_market(db: AsyncSession, req: MarketRequest, user: Optional[User]) -> Dict[str, Any]:
    result = _market(req.crop, req.days, req.location)
    if user and result.get("success"):
        await _save(db, MarketPrediction(
            farmer_id=user.farmer.id if user.farmer else None,
            crop=req.crop, location=req.location, forecast_days=req.days,
            current_price=result["current_price"], trend=result["trend"],
            recommendation_action=result["recommendation"]["action"],
            predictions_json=result["predictions"],
            data_source=result["data_source"]["current_price_source"],
        ))
    return result


async def run_advisor(db: AsyncSession, req: AdvisorRequest, user: Optional[User]) -> Dict[str, Any]:
    return _advisor(req.soil_type, req.land_acres, req.budget, req.season)


async def _save(db: AsyncSession, obj):
    db.add(obj)
    await db.commit()
