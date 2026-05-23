"""OTP service: generate, store in-memory, verify, and send via Fast2SMS."""

import os
import random
import time
from typing import Dict, Tuple

import httpx

_otp_store: Dict[str, Dict] = {}
OTP_EXPIRE_SECONDS = 300
OTP_LENGTH = 6

FAST2SMS_API_KEY = "FUVQhKv1EAfkLz7mX6OealHW2bp48udyqIBD9J0TY5twocSCRiziNlv0AIUh5rgQk4ZnbGdF6qT7exoc"


def _cleanup_expired():
    now = time.time()
    for k in [k for k, v in _otp_store.items() if v["expires_at"] < now]:
        del _otp_store[k]


def generate_otp(length: int = OTP_LENGTH) -> str:
    return str(random.randint(10 ** (length - 1), 10**length - 1))


def store_otp(phone: str, otp: str) -> None:
    _cleanup_expired()
    _otp_store[phone] = {"otp": otp, "expires_at": time.time() + OTP_EXPIRE_SECONDS}


def verify_otp(phone: str, code: str) -> Tuple[bool, str]:
    _cleanup_expired()
    record = _otp_store.get(phone)
    if record is None:
        return False, "No OTP sent or OTP expired"
    if record["otp"] != code:
        return False, "Invalid OTP"
    del _otp_store[phone]
    return True, "OTP verified"


async def send_otp_via_gateway(phone: str, otp: str) -> Tuple[bool, str]:
    """Send OTP directly via Fast2SMS API. Falls back to console on failure."""
    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    message = f"Your Trinetra Agro AI OTP is: {otp}. Valid for 5 minutes."

    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "numbers": digits,
    }
    headers = {
        "authorization": FAST2SMS_API_KEY,
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.post(
                "https://www.fast2sms.com/dev/bulkV2",
                json=payload,
                headers=headers,
            )
            if resp.status_code == 200:
                data = resp.json()
                if data.get("return"):
                    return True, "sent via Fast2SMS"
            # Fast2SMS returned error — log and fall back to console
            print(f"\n=== OTP for {phone}: {otp} (Fast2SMS unavailable: {resp.text[:200]}) ===\n")
            return True, "console fallback (SMS provider needs recharge)"
    except Exception as e:
        print(f"\n=== OTP for {phone}: {otp} (Fast2SMS error: {e}) ===\n")
        return True, f"console fallback (Fast2SMS error: {e})"
