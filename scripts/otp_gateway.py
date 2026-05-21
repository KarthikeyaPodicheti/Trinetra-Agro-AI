#!/usr/bin/env python3
"""Simple OTP webhook gateway for SMS delivery.

Receives POST /send-otp with JSON:
{
  "phone": "+919876543210",
  "otp": "123456",
  "message": "...",
  "sender": "Trinetra Agro AI"
}

Providers:
- console (default): logs OTP to terminal
- fast2sms: sends SMS via Fast2SMS API
- twilio: sends SMS via Twilio REST API
"""

from __future__ import annotations

import argparse
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, Tuple

import requests


def _send_fast2sms(phone: str, message: str) -> Tuple[bool, str]:
    api_key = os.getenv("FAST2SMS_API_KEY", "").strip()
    if not api_key:
        return False, "FAST2SMS_API_KEY not configured"

    digits = "".join(ch for ch in phone if ch.isdigit())
    if len(digits) == 12 and digits.startswith("91"):
        digits = digits[2:]

    payload = {
        "route": "q",
        "message": message,
        "language": "english",
        "numbers": digits,
    }
    headers = {
        "authorization": api_key,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post("https://www.fast2sms.com/dev/bulkV2", json=payload, headers=headers, timeout=10)
        if resp.status_code == 200:
            return True, "fast2sms sent"
        return False, f"fast2sms status {resp.status_code}: {resp.text[:200]}"
    except Exception as exc:
        return False, f"fast2sms error: {exc}"


def _send_twilio(phone: str, message: str) -> Tuple[bool, str]:
    sid = os.getenv("TWILIO_ACCOUNT_SID", "").strip()
    token = os.getenv("TWILIO_AUTH_TOKEN", "").strip()
    from_number = os.getenv("TWILIO_FROM_NUMBER", "").strip()
    if not sid or not token or not from_number:
        return False, "TWILIO_ACCOUNT_SID/TWILIO_AUTH_TOKEN/TWILIO_FROM_NUMBER required"

    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    data = {
        "To": phone,
        "From": from_number,
        "Body": message,
    }
    try:
        resp = requests.post(url, data=data, auth=(sid, token), timeout=10)
        if 200 <= resp.status_code < 300:
            return True, "twilio sent"
        return False, f"twilio status {resp.status_code}: {resp.text[:200]}"
    except Exception as exc:
        return False, f"twilio error: {exc}"


def deliver_sms(phone: str, otp: str, message: str) -> Tuple[bool, str]:
    provider = os.getenv("OTP_PROVIDER", "console").strip().lower()
    if provider == "console":
        print(f"[OTP-CONSOLE] phone={phone} otp={otp} message={message}")
        return True, "console logged"
    if provider == "fast2sms":
        return _send_fast2sms(phone, message)
    if provider == "twilio":
        return _send_twilio(phone, message)
    return False, f"Unsupported OTP_PROVIDER: {provider}"


class OtpHandler(BaseHTTPRequestHandler):
    def _write_json(self, status: int, payload: Dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        expected_path = os.getenv("OTP_WEBHOOK_PATH", "/send-otp")
        if self.path != expected_path:
            self._write_json(404, {"success": False, "error": "Not found"})
            return

        bearer = os.getenv("OTP_GATEWAY_BEARER_TOKEN", "").strip()
        if bearer:
            auth = self.headers.get("Authorization", "")
            if auth != f"Bearer {bearer}":
                self._write_json(401, {"success": False, "error": "Unauthorized"})
                return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
        except Exception:
            self._write_json(400, {"success": False, "error": "Invalid JSON payload"})
            return

        phone = str(payload.get("phone", "")).strip()
        otp = str(payload.get("otp", "")).strip()
        message = str(payload.get("message", "")).strip()
        if not phone or not otp or not message:
            self._write_json(400, {"success": False, "error": "phone, otp, and message are required"})
            return

        ok, detail = deliver_sms(phone, otp, message)
        if ok:
            self._write_json(200, {"success": True, "detail": detail})
        else:
            self._write_json(502, {"success": False, "error": detail})

    def log_message(self, _format: str, *_args) -> None:
        return


def main() -> None:
    parser = argparse.ArgumentParser(description="OTP webhook gateway")
    parser.add_argument("--host", default=os.getenv("OTP_GATEWAY_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("OTP_GATEWAY_PORT", "8081")))
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), OtpHandler)
    path = os.getenv("OTP_WEBHOOK_PATH", "/send-otp")
    provider = os.getenv("OTP_PROVIDER", "console")
    print(f"OTP gateway listening on http://{args.host}:{args.port}{path} (provider={provider})")
    server.serve_forever()


if __name__ == "__main__":
    main()
