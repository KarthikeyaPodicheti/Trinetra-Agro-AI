"""Unit tests for backend.auth.otp_service — pure logic, no network."""

import asyncio

from backend.auth import otp_service
from backend.auth.otp_service import (
    generate_otp,
    normalize_phone,
    send_otp_via_gateway,
    store_otp,
    verify_otp,
)


class TestNormalizePhone:
    def test_plain_ten_digit(self):
        assert normalize_phone("9876543210") == "9876543210"

    def test_plus91_stripped(self):
        assert normalize_phone("+919876543210") == "9876543210"

    def test_dashes_spaces_stripped(self):
        assert normalize_phone("+91 98765 43210") == "9876543210"

    def test_other_country_kept(self):
        assert normalize_phone("+15551234567") == "15551234567"


class TestGenerateOtp:
    def test_six_digit_numeric(self):
        for _ in range(20):
            otp = generate_otp()
            assert len(otp) == 6
            assert otp.isdigit()


class TestStoreVerify:
    def test_verify_success(self):
        store_otp("9876543210", "123456")
        ok, _ = verify_otp("9876543210", "123456")
        assert ok is True

    def test_verify_normalizes_phone(self):
        store_otp("+919876543210", "111222")
        ok, _ = verify_otp("9876543210", "111222")
        assert ok is True

    def test_wrong_code(self):
        store_otp("9876543210", "123456")
        ok, msg = verify_otp("9876543210", "000000")
        assert ok is False
        assert "Invalid" in msg

    def test_no_otp_sent(self):
        ok, msg = verify_otp("9999999999", "123456")
        assert ok is False
        assert "No OTP" in msg

    def test_expired_otp(self, monkeypatch):
        store_otp("9876543210", "123456")
        otp_service._otp_store["9876543210"]["expires_at"] = 0
        ok, msg = verify_otp("9876543210", "123456")
        assert ok is False
        assert "expired" in msg.lower() or "No OTP" in msg


class TestSendOtpViaGateway:
    def test_console_fallback_without_key(self, capsys):
        ok, detail = asyncio.run(send_otp_via_gateway("9876543210", "123456", api_key=""))
        assert ok is True
        assert "console fallback" in detail
        captured = capsys.readouterr()
        assert "123456" in captured.out

    def test_error_does_not_crash(self, monkeypatch):
        class BoomClient:
            def __init__(self, *a, **k):
                pass

            async def __aenter__(self):
                raise Exception("network down")

            async def __aexit__(self, *a):
                pass

            async def post(self, *a, **k):
                raise Exception("boom")

        monkeypatch.setattr(otp_service.httpx, "AsyncClient", BoomClient)
        ok, detail = asyncio.run(send_otp_via_gateway("9876543210", "123456", api_key="secret"))
        assert ok is True
        assert "console fallback" in detail