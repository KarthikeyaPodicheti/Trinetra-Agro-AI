"""Smoke tests for system + mandi + ai endpoints (hermetic — no real keys needed)."""


class TestSystem:
    def test_health(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "healthy"
        assert body["version"]

    def test_root(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert resp.json()["app"] == "Trinetra Agro AI"


class TestMandiEndpoint:
    def test_crops_list(self, client):
        resp = client.get("/mandi/crops")
        assert resp.status_code == 200
        assert len(resp.json()["crops"]) > 0

    def test_prices_without_key_graceful(self, client):
        resp = client.get("/mandi/prices", params={"crop": "Onion"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is False
        assert "DATA_GOV_API_KEY" in body["error"]


class TestAiEndpoint:
    def test_market_forecast_uses_synthetic_fallback(self, client):
        resp = client.post("/ai/market", json={"crop": "rice", "days": 14, "location": "Hyderabad"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["success"] is True
        assert body["crop"] == "Rice"
        assert "synthetic" in body["data_source"]["current_price_source"].lower()

    def test_market_forecast_unsupported_crop(self, client):
        resp = client.post("/ai/market", json={"crop": "dragonfruit", "days": 14})
        assert resp.status_code == 200
        assert resp.json()["success"] is False