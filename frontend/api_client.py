"""HTTP client for Trinetra Agro AI backend API — with JWT validation and auto-refresh."""

import base64
import json
import time
from typing import Optional

import httpx
import streamlit as st

API_BASE = "http://localhost:8000"

# How many seconds before expiry to consider token "expired"
TOKEN_GRACE_SECONDS = 60


def _decode_jwt_payload(token: str) -> Optional[dict]:
    """Decode JWT payload without verification (just to check expiry)."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        payload = parts[1] + "=="
        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception:
        return None


def _token_expired(token: str) -> bool:
    """Check if JWT token is expired based on its 'exp' claim."""
    payload = _decode_jwt_payload(token)
    if payload is None:
        return True
    exp = payload.get("exp", 0)
    return time.time() > (exp - TOKEN_GRACE_SECONDS)


def _refresh_access_token() -> bool:
    """Use refresh token to get a new access token."""
    refresh = st.session_state.get("refresh_token")
    if not refresh:
        return False
    try:
        r = httpx.post(f"{API_BASE}/auth/refresh", json={"refresh_token": refresh}, timeout=10.0)
        if r.status_code == 200:
            data = r.json()
            st.session_state["access_token"] = data["access_token"]
            st.session_state["refresh_token"] = data["refresh_token"]
            st.session_state["user"] = _fetch_me()
            return True
    except Exception:
        pass
    return False


def _fetch_me() -> Optional[dict]:
    """Fetch current user info from backend."""
    token = st.session_state.get("access_token")
    if not token:
        return None
    try:
        r = httpx.get(f"{API_BASE}/auth/me", headers={"Authorization": f"Bearer {token}"}, timeout=10.0)
        return r.json() if r.status_code == 200 else None
    except Exception:
        return None


def _ensure_valid_token() -> Optional[str]:
    """Return valid access token, refreshing if needed. Returns None if fully expired."""
    token = st.session_state.get("access_token")
    if not token:
        return None

    if _token_expired(token):
        if not _refresh_access_token():
            return None
        token = st.session_state.get("access_token")
    return token


def _headers() -> dict:
    h = {"Content-Type": "application/json"}
    token = _ensure_valid_token()
    if token:
        h["Authorization"] = f"Bearer {token}"
    return h


def api_post(path: str, data: dict = None, files: dict = None) -> dict:
    try:
        if files:
            h = {"Authorization": _headers().get("Authorization", "")}
            r = httpx.post(f"{API_BASE}{path}", data=data, files=files, headers=h, timeout=60.0)
        else:
            r = httpx.post(f"{API_BASE}{path}", json=data or {}, headers=_headers(), timeout=45.0)
        if r.status_code == 401 and _refresh_access_token():
            # Retry once after refresh
            h = {"Authorization": f"Bearer {st.session_state.get('access_token')}"}
            r = httpx.post(f"{API_BASE}{path}", json=data or {}, headers=h, timeout=45.0)
        return r.json() if r.status_code in (200, 201) else {"error": r.text}
    except Exception as e:
        return {"error": str(e)}


def api_get(path: str) -> dict:
    try:
        r = httpx.get(f"{API_BASE}{path}", headers=_headers(), timeout=10.0)
        return r.json() if r.status_code == 200 else {"error": r.text}
    except Exception as e:
        return {"error": str(e)}


def login(email: str, password: str) -> bool:
    r = httpx.post(f"{API_BASE}/auth/login", json={"email": email, "password": password}, timeout=10.0)
    if r.status_code == 200:
        data = r.json()
        st.session_state["access_token"] = data["access_token"]
        st.session_state["refresh_token"] = data["refresh_token"]
        user_data = _fetch_me()
        st.session_state["user"] = user_data
        st.session_state["login_time"] = time.time()
        return True
    return False


def register(email: str, password: str, full_name: str = "") -> bool:
    r = httpx.post(f"{API_BASE}/auth/register", json={"email": email, "password": password, "full_name": full_name}, timeout=10.0)
    if r.status_code in (200, 201):
        return login(email, password)
    return False


def logout():
    for k in ["access_token", "refresh_token", "user", "login_time", "authenticated"]:
        st.session_state.pop(k, None)


def verify_session() -> bool:
    """Verify the current session is still valid by checking the /auth/me endpoint.
    Call this on every page load to prevent bypassing auth."""
    if not st.session_state.get("access_token"):
        return False
    user = _fetch_me()
    if user is None:
        return False
    st.session_state["user"] = user
    return True
