"""Integration tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)

BASE_EMAIL = "test_int@farm.com"
BASE_PW = "testpassword123"


class TestAuthFlow:
    def test_register(self):
        r = client.post("/auth/register", json={"email": BASE_EMAIL, "password": BASE_PW, "full_name": "Test Farmer"})
        assert r.status_code in (200, 201)
        data = r.json()
        assert data["email"] == BASE_EMAIL

    def test_login(self):
        # User deleted by conftest, create then login
        client.post("/auth/register", json={"email": "logintest@farm.com", "password": BASE_PW})
        r = client.post("/auth/login", json={"email": "logintest@farm.com", "password": BASE_PW})
        assert r.status_code == 200
        data = r.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_me(self):
        client.post("/auth/register", json={"email": "metest@farm.com", "password": BASE_PW})
        login_r = client.post("/auth/login", json={"email": "metest@farm.com", "password": BASE_PW})
        token = login_r.json()["access_token"]
        r = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert r.status_code == 200
        assert r.json()["email"] == "metest@farm.com"

    def test_invalid_login(self):
        r = client.post("/auth/login", json={"email": "nobody@farm.com", "password": "wrong"})
        assert r.status_code == 401

    def test_duplicate_register(self):
        client.post("/auth/register", json={"email": "dup@farm.com", "password": "test123456"})
        r = client.post("/auth/register", json={"email": "dup@farm.com", "password": "test123456"})
        assert r.status_code == 409


class TestHealth:
    def test_health_check(self):
        r = client.get("/health")
        assert r.status_code == 200
        assert r.json()["status"] == "healthy"


class TestAIEndpoints:
    def test_irrigation(self):
        r = client.post("/ai/irrigation", json={"crop": "rice", "land_acres": 5})
        assert r.status_code == 200
        assert r.json()["success"] is True

    def test_profit(self):
        r = client.post("/ai/profit", json={"crop": "wheat", "land_acres": 3})
        assert r.status_code == 200
        assert "profit" in r.json()

    def test_risk(self):
        r = client.post("/ai/risk", json={"crop": "cotton", "soil_type": "black cotton"})
        assert r.status_code == 200
        assert "risk_score" in r.json()

    def test_yield(self):
        r = client.post("/ai/yield", json={"crop": "rice", "land_acres": 3})
        assert r.status_code == 200
        assert "estimates" in r.json()

    def test_market(self):
        r = client.post("/ai/market", json={"crop": "tomato", "days": 14})
        assert r.status_code == 200
        assert "predictions" in r.json()

    def test_advisor(self):
        r = client.post("/ai/advisor", json={"soil_type": "loamy", "land_acres": 5, "budget": 50000})
        assert r.status_code == 200
        assert "primary_recommendations" in r.json()
