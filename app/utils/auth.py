"""OTP authentication helpers for farmer login."""

from __future__ import annotations

import hashlib
import os
import random
import time
from typing import Dict, Optional, Tuple

import requests


def normalize_phone(phone: str) -> str:
    digits = "".join(ch for ch in (phone or "") if ch.isdigit())
    if len(digits) == 10:
        return f"+91{digits}"
    if len(digits) == 12 and digits.startswith("91"):
        return f"+{digits}"
    if len(digits) > 10 and not digits.startswith("+"):
        return f"+{digits}"
    return phone.strip()


def _otp_secret() -> str:
    return os.getenv("OTP_SECRET", os.getenv("SECRET_KEY", "trinetra-otp-secret"))


def _otp_hash(phone: str, otp: str) -> str:
    payload = f"{_otp_secret()}::{phone}::{otp}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _otp_message(otp: str) -> str:
    sender = os.getenv("OTP_SENDER_NAME", "Trinetra Agro AI")
    return f"{sender} login code: {otp}. Valid for 5 minutes. Do not share this code."


def _send_via_webhook(phone: str, otp: str) -> Tuple[bool, str]:
    url = os.getenv("OTP_WEBHOOK_URL", "").strip()
    if not url:
        return False, "OTP_WEBHOOK_URL not configured"

    headers = {"Content-Type": "application/json"}
    bearer = os.getenv("OTP_WEBHOOK_BEARER_TOKEN", "").strip()
    if bearer:
        headers["Authorization"] = f"Bearer {bearer}"

    payload = {
        "phone": phone,
        "otp": otp,
        "message": _otp_message(otp),
        "sender": os.getenv("OTP_SENDER_NAME", "Trinetra Agro AI"),
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=8)
        if 200 <= resp.status_code < 300:
            return True, "sent"
        return False, f"webhook status {resp.status_code}"
    except Exception as exc:
        return False, f"webhook error: {exc}"


def issue_otp(phone: str, auth_state: Dict) -> Dict:
    now = int(time.time())
    expiry = int(os.getenv("OTP_EXPIRY_SEC", "300"))
    resend_wait = int(os.getenv("OTP_RESEND_INTERVAL_SEC", "45"))
    allow_dev = os.getenv("OTP_ALLOW_DEV_FALLBACK", "false").strip().lower() in {"1", "true", "yes", "on"}

    existing = auth_state.get("challenge") or {}
    next_send_at = int(existing.get("next_send_at", 0))
    if now < next_send_at:
        return {
            "success": False,
            "error": f"Please wait {next_send_at - now}s before requesting another OTP.",
        }

    phone_norm = normalize_phone(phone)
    otp = f"{random.randint(0, 999999):06d}"
    sent, reason = _send_via_webhook(phone_norm, otp)
    channel = "webhook"

    if not sent and allow_dev:
        sent = True
        channel = "dev"

    if not sent:
        return {
            "success": False,
            "error": f"OTP send failed: {reason}",
        }

    auth_state["challenge"] = {
        "phone": phone_norm,
        "otp_hash": _otp_hash(phone_norm, otp),
        "expires_at": now + expiry,
        "next_send_at": now + resend_wait,
        "attempts": 0,
        "channel": channel,
    }

    result = {
        "success": True,
        "phone": phone_norm,
        "expires_in": expiry,
        "channel": channel,
    }
    if channel == "dev":
        result["dev_otp"] = otp
    return result


def verify_otp(phone: str, otp: str, auth_state: Dict) -> Dict:
    challenge = auth_state.get("challenge") or {}
    if not challenge:
        return {"success": False, "error": "No active OTP challenge. Request a new OTP."}

    now = int(time.time())
    if now > int(challenge.get("expires_at", 0)):
        auth_state.pop("challenge", None)
        return {"success": False, "error": "OTP expired. Request a new code."}

    expected_phone = challenge.get("phone")
    if normalize_phone(phone) != expected_phone:
        return {"success": False, "error": "Phone mismatch. Use the same number used for OTP request."}

    max_attempts = int(os.getenv("OTP_MAX_ATTEMPTS", "5"))
    attempts = int(challenge.get("attempts", 0)) + 1
    challenge["attempts"] = attempts
    auth_state["challenge"] = challenge
    if attempts > max_attempts:
        auth_state.pop("challenge", None)
        return {"success": False, "error": "Too many invalid attempts. Request a new OTP."}

    if _otp_hash(expected_phone, otp.strip()) != challenge.get("otp_hash"):
        remain = max(0, max_attempts - attempts)
        return {"success": False, "error": f"Invalid OTP. Attempts left: {remain}"}

    auth_state["authenticated"] = True
    auth_state["phone"] = expected_phone
    auth_state.pop("challenge", None)
    return {"success": True, "phone": expected_phone}


def logout(auth_state: Dict) -> None:
    auth_state["authenticated"] = False
    auth_state.pop("phone", None)
    auth_state.pop("challenge", None)
