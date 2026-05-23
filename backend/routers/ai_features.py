"""AI Feature Routers — market forecasting and crop advisor."""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.dependencies import get_db, get_optional_user
from backend.models import User
from backend.schemas.ai_features import (
    AdvisorRequest, IrrigationRequest, MarketRequest,
    ProfitRequest, RiskRequest, YieldRequest,
)
from backend.services.ai_service import run_advisor, run_market

router = APIRouter(prefix="/ai", tags=["ai-features"])


@router.post("/market")
async def market_forecast(req: MarketRequest, db: AsyncSession = Depends(get_db),
                          user: Optional[User] = Depends(get_optional_user)):
    return await run_market(db, req, user)


@router.post("/advisor")
async def crop_advisor(req: AdvisorRequest, db: AsyncSession = Depends(get_db),
                       user: Optional[User] = Depends(get_optional_user)):
    return await run_advisor(db, req, user)


@router.post("/irrigation")
async def irrigation_plan(req: IrrigationRequest):
    from ai_engine.irrigation_ai.engine import irrigation_plan as _plan
    return _plan(req.crop, req.land_acres, req.growth_stage)


@router.post("/profit")
async def profit_analysis(req: ProfitRequest):
    from ai_engine.profit_engine.engine import predict_profit as _profit
    return _profit(req.crop, req.land_acres, req.irrigation)


@router.post("/risk")
async def risk_assessment(req: RiskRequest):
    from ai_engine.risk_engine.engine import assess_risk as _risk
    return _risk(req.crop, req.soil_type, req.land_acres, req.budget, req.irrigation)


@router.post("/yield")
async def yield_prediction(req: YieldRequest):
    from ai_engine.yield_prediction.engine import predict_yield as _yield
    return _yield(req.crop, req.land_acres, req.soil_type, req.irrigation)
