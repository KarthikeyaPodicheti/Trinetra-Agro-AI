"""Unit tests for JWT and password hashing."""

import pytest
from backend.core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token


class TestSecurity:
    def test_password_hash_and_verify(self):
        pw = "testpass123"
        hashed = hash_password(pw)
        assert hashed != pw
        assert verify_password(pw, hashed)
        assert not verify_password("wrongpass", hashed)

    def test_access_token_creation_and_decode(self):
        token = create_access_token("user123")
        payload = decode_token(token)
        assert payload.get("sub") == "user123"
        assert payload.get("type") == "access"
        assert "exp" in payload

    def test_refresh_token_type(self):
        token = create_refresh_token("user123")
        payload = decode_token(token)
        assert payload.get("type") == "refresh"

    def test_invalid_token_returns_empty(self):
        assert decode_token("invalid.token.string") == {}

    def test_expired_token(self):
        from datetime import timedelta
        token = create_access_token("user123", expires_delta=timedelta(seconds=-1))
        payload = decode_token(token)
        assert payload == {}
