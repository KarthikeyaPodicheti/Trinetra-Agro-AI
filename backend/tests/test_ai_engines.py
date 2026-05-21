"""Unit tests for AI engine modules."""

import pytest

from ai_engine.irrigation_ai.engine import irrigation_plan, SUPPORTED_CROPS as IRRIG_CROPS
from ai_engine.profit_engine.engine import predict_profit, SUPPORTED_CROPS as PROFIT_CROPS
from ai_engine.risk_engine.engine import assess_risk
from ai_engine.yield_prediction.engine import predict_yield, SUPPORTED_CROPS as YIELD_CROPS
from ai_engine.market_forecasting.engine import predict_prices, SUPPORTED_CROPS as MARKET_CROPS
from ai_engine.recommendation_engine.engine import get_recommendations


class TestIrrigationAI:
    def test_plan_success(self):
        result = irrigation_plan("rice", 5.0, "Vegetative (20-50%)")
        assert result["success"] is True
        assert result["crop"] == "Rice"
        assert result["water_needs"]["daily_litres"] > 0

    def test_unsupported_crop_returns_error(self):
        result = irrigation_plan("unknown_crop")
        assert result["success"] is False

    def test_all_supported_crops(self):
        for crop in IRRIG_CROPS:
            result = irrigation_plan(crop, 1.0)
            assert result["success"] is True, f"Failed for {crop}"


class TestProfitAI:
    def test_profit_success(self):
        result = predict_profit("wheat", 5.0)
        assert result["success"] is True
        assert "profit" in result
        assert "roi_percent" in result

    def test_unsupported_crop(self):
        result = predict_profit("unknown")
        assert result["success"] is False


class TestRiskAI:
    def test_risk_assessment(self):
        result = assess_risk("cotton", "black cotton", 5.0, 100000, True)
        assert result["success"] is True
        assert 0 <= result["risk_score"] <= 100
        assert result["risk_level"] in ("Low", "Medium", "High")

    def test_risk_breakdown_five_dims(self):
        result = assess_risk("rice")
        bd = result["breakdown"]
        assert set(bd.keys()) == {"disease_risk", "market_risk", "water_risk", "budget_risk", "land_risk"}


class TestYieldAI:
    def test_yield_success(self):
        result = predict_yield("rice", 3.0, "loamy", True)
        assert result["success"] is True
        assert result["estimates"]["moderate"] > 0

    def test_soil_multiplier_effect(self):
        good = predict_yield("wheat", 1.0, "alluvial", True)
        bad = predict_yield("wheat", 1.0, "sandy", True)
        assert good["estimates"]["moderate"] > bad["estimates"]["moderate"]


class TestMarketAI:
    def test_market_forecast(self):
        result = predict_prices("tomato", 14)
        assert result["success"] is True
        assert len(result["predictions"]["prices"]) == 14

    def test_trend_is_valid(self):
        result = predict_prices("rice")
        assert result["trend"] in ("upward", "downward", "stable")


class TestAdvisorAI:
    def test_recommendations(self):
        result = get_recommendations("black cotton", 10, 100000, "kharif")
        assert result["success"] is True
        assert len(result["primary_recommendations"]) >= 1
        assert "name" in result["primary_recommendations"][0]
