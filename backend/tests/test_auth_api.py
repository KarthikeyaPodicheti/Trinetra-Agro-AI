"""Integration tests for the auth API — runs against SQLite via TestClient."""

import uuid


def _email():
    return f"user-{uuid.uuid4().hex[:10]}@test.com"


def _register(client, email=None, password="supersecret123", phone=None):
    return client.post(
        "/auth/register",
        json={"email": email or _email(), "password": password, "full_name": "Test User", "phone": phone},
    )


class TestRegister:
    def test_register_success(self, client):
        resp = _register(client)
        assert resp.status_code == 201
        body = resp.json()
        assert body["email"].endswith("@test.com")
        assert "id" in body
        assert body["is_active"] is True

    def test_register_short_password_rejected(self, client):
        resp = _register(client, password="short")
        assert resp.status_code == 422

    def test_register_duplicate_email_conflict(self, client):
        email = _email()
        assert _register(client, email=email).status_code == 201
        resp = _register(client, email=email)
        assert resp.status_code == 409

    def test_register_normalizes_phone(self, client):
        resp = _register(client, phone="+919876543210")
        assert resp.status_code == 201
        assert resp.json()["phone"] == "9876543210"


class TestLogin:
    def test_login_success_returns_tokens(self, client):
        email = _email()
        _register(client, email=email)
        resp = client.post("/auth/login", json={"email": email, "password": "supersecret123"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["token_type"] == "bearer"
        assert body["access_token"]
        assert body["refresh_token"]
        assert body["expires_in"] > 0

    def test_login_wrong_password(self, client):
        email = _email()
        _register(client, email=email)
        resp = client.post("/auth/login", json={"email": email, "password": "wrong-password"})
        assert resp.status_code == 401

    def test_login_unknown_email(self, client):
        resp = client.post("/auth/login", json={"email": _email(), "password": "supersecret123"})
        assert resp.status_code == 401


class TestMe:
    def test_me_with_valid_token(self, client):
        email = _email()
        _register(client, email=email)
        tokens = client.post("/auth/login", json={"email": email, "password": "supersecret123"}).json()
        resp = client.get("/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
        assert resp.status_code == 200
        assert resp.json()["email"] == email

    def test_me_without_token(self, client):
        resp = client.get("/auth/me")
        assert resp.status_code == 401

    def test_me_with_garbage_token(self, client):
        resp = client.get("/auth/me", headers={"Authorization": "Bearer garbage.token.here"})
        assert resp.status_code == 401


class TestRefresh:
    def test_refresh_returns_new_tokens(self, client):
        email = _email()
        _register(client, email=email)
        tokens = client.post("/auth/login", json={"email": email, "password": "supersecret123"}).json()
        resp = client.post("/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
        assert resp.status_code == 200
        assert resp.json()["access_token"]

    def test_refresh_rejects_access_token(self, client):
        email = _email()
        _register(client, email=email)
        tokens = client.post("/auth/login", json={"email": email, "password": "supersecret123"}).json()
        resp = client.post("/auth/refresh", json={"refresh_token": tokens["access_token"]})
        assert resp.status_code == 401

    def test_refresh_rejects_garbage(self, client):
        resp = client.post("/auth/refresh", json={"refresh_token": "garbage.token.here"})
        assert resp.status_code == 401


class TestOtpEndpoints:
    def test_send_otp_unknown_phone_404(self, client):
        resp = client.post("/auth/send-otp", json={"phone": "9999999999"})
        assert resp.status_code == 404

    def test_send_otp_registered_phone(self, client):
        phone = f"98{uuid.uuid4().hex[:8]}"
        _register(client, phone=phone)
        resp = client.post("/auth/send-otp", json={"phone": phone})
        assert resp.status_code == 200
        # development environment exposes the OTP in the response
        assert "otp" in resp.json()

    def test_verify_otp_success(self, client):
        phone = f"97{uuid.uuid4().hex[:8]}"
        _register(client, phone=phone)
        otp = client.post("/auth/send-otp", json={"phone": phone}).json()["otp"]
        resp = client.post("/auth/verify-otp", json={"phone": phone, "otp": otp})
        assert resp.status_code == 200
        assert resp.json()["access_token"]