from ai_modules.market_prediction import MarketPredictor


def test_market_prediction_supported_crop_returns_success():
    predictor = MarketPredictor()
    result = predictor.predict_prices("rice", days=7, location="Hyderabad")

    assert result["success"] is True
    assert result["crop"] == "rice"
    assert result["days_predicted"] == 7
    assert len(result["predictions"]["prices"]) == 7


def test_market_prediction_unsupported_crop_fails_cleanly():
    predictor = MarketPredictor()
    result = predictor.predict_prices("dragonfruit", days=7)

    assert result["success"] is False
    assert "not supported" in result["error"].lower()
