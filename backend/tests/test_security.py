"""Unit tests for backend.core.security — bcrypt + JWT."""

from datetime import timedelta

from jose import jwt

from backend.core.config import get_settings
from backend.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)

settings = get_settings()


class TestPasswordHashing:
    def test_roundtrip(self):
        hashed = hash_password("supersecret123")
        assert hashed != "supersecret123"
        assert verify_password("supersecret123", hashed) is True

    def test_wrong_password(self):
        hashed = hash_password("supersecret123")
        assert verify_password("wrong", hashed) is False

    def test_hashes_are_salted(self):
        assert hash_password("same") != hash_password("same")


class TestTokenCreation:
    def test_access_token_decodes(self):
        token = create_access_token("user-123")
        payload = decode_token(token)
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"
        assert "exp" in payload

    def test_refresh_token_type(self):
        token = create_refresh_token("user-123")
        payload = decode_token(token)
        assert payload["type"] == "refresh"
        assert payload["sub"] == "user-123"

    def test_access_token_signature_valid(self):
        token = create_access_token("user-123")
        claims = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        assert claims["sub"] == "user-123"


class TestTokenValidation:
    def test_invalid_signature(self):
        token = create_access_token("user-123")
        tampered = token[:-4] + "abcd"
        assert decode_token(tampered) == {}

    def test_garbage_token(self):
        assert decode_token("not.a.jwt") == {}

    def test_expired_token(self):
        token = create_access_token("user-123", expires_delta=timedelta(seconds=-10))
        assert decode_token(token) == {}