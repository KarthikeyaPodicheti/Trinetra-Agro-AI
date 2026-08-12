"""Unit tests for backend.services.mandi_service — hermetic, no network."""

import asyncio

from backend.services import mandi_service
from backend.services.mandi_service import (
    _calculate_trend,
    _generate_recommendation,
    _parse_records,
    fetch_mandi_prices,
)


def _price(price, date="2026-01-01"):
    return {
        "mandi": "Lasalgaon",
        "crop": "Onion",
        "price_per_quintal": price,
        "state": "Maharashtra",
        "district": "Nashik",
        "date": date,
    }


class TestNoApiKey:
    def test_returns_graceful_error(self):
        result = asyncio.run(fetch_mandi_prices("Onion", api_key=None, limit=10))
        assert result["success"] is False
        assert "DATA_GOV_API_KEY" in result["error"]


class TestParseRecords:
    def test_filters_zero_and_invalid_prices(self):
        records = [
            {"modal_price": "1500", "market": "M1", "commodity": "Onion", "state": "S", "district": "D", "arrival_date": "2026-01-02"},
            {"modal_price": "0", "market": "M2", "commodity": "Onion", "state": "S", "district": "D", "arrival_date": "2026-01-01"},
            {"modal_price": "abc", "market": "M3", "commodity": "Onion", "state": "S", "district": "D", "arrival_date": "2026-01-03"},
        ]
        prices = _parse_records(records, "Onion")
        assert len(prices) == 1
        assert prices[0]["price_per_quintal"] == 1500.0

    def test_empty_records(self):
        assert _parse_records([], "Onion") == []


class TestTrend:
    def test_rising(self):
        # newest-first order (as _parse_records returns): newest price highest
        prices = [_price(1600 - i * 100, f"2026-01-{i:02d}") for i in range(7)]
        assert _calculate_trend(prices) == "rising"

    def test_falling(self):
        prices = [_price(1000 + i * 100, f"2026-01-{i:02d}") for i in range(7)]
        assert _calculate_trend(prices) == "falling"

    def test_stable(self):
        prices = [_price(1000, f"2026-01-{i:02d}") for i in range(1, 8)]
        assert _calculate_trend(prices) == "stable"

    def test_too_few_points(self):
        assert _calculate_trend([_price(1000)]) == "stable"


class TestRecommendation:
    def test_no_data(self):
        rec = _generate_recommendation("stable", [])
        assert rec["action"] == "no_data"

    def test_rising_holds(self):
        prices = [_price(1000, f"2026-01-{i:02d}") for i in range(1, 4)]
        rec = _generate_recommendation("rising", prices)
        assert rec["action"] == "hold"

    def test_falling_sells(self):
        prices = [_price(1000, f"2026-01-{i:02d}") for i in range(1, 4)]
        rec = _generate_recommendation("falling", prices)
        assert rec["action"] == "sell_now"

    def test_stable_monitors(self):
        prices = [_price(1000, f"2026-01-{i:02d}") for i in range(1, 4)]
        rec = _generate_recommendation("stable", prices)
        assert rec["action"] == "monitor"


class TestCache:
    def test_cache_hit_avoids_fetch(self, monkeypatch):
        calls = {"n": 0}

        class FakeResponse:
            status_code = 200

            def json(self):
                return {"records": [{"modal_price": "1500", "market": "M", "commodity": "Onion", "state": "S", "district": "D", "arrival_date": "2026-01-01"}]}

        class FakeClient:
            def __init__(self, *a, **k):
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                pass

            async def get(self, *a, **k):
                calls["n"] += 1
                return FakeResponse()

        monkeypatch.setattr(mandi_service.httpx, "AsyncClient", FakeClient)
        mandi_service._cache.clear()

        async def _run():
            r1 = await fetch_mandi_prices("Onion", api_key="k", limit=10)
            r2 = await fetch_mandi_prices("Onion", api_key="k", limit=10)
            return r1, r2

        r1, r2 = asyncio.run(_run())
        assert calls["n"] == 1
        assert r1["success"] is True and r2["success"] is True
        assert r1["prices"][0]["price_per_quintal"] == 1500.0

    def test_cache_miss_on_network_error(self, monkeypatch):
        class BoomClient:
            def __init__(self, *a, **k):
                pass

            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                pass

            async def get(self, *a, **k):
                raise Exception("timeout")

        monkeypatch.setattr(mandi_service.httpx, "AsyncClient", BoomClient)
        mandi_service._cache.clear()

        result = asyncio.run(fetch_mandi_prices("Onion", api_key="k", limit=10))
        assert result["success"] is True
        assert len(result["prices"]) > 0  # fallback synthetic data