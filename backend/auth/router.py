"""Auth router: POST /register, /login, /refresh, /send-otp, /verify-otp, GET /me."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth.otp_service import generate_otp, normalize_phone, send_otp_via_gateway, store_otp, verify_otp
from backend.auth.service import login_user, refresh_access_token, register_user
from backend.core.dependencies import get_current_user, get_db
from backend.core.security import create_access_token, create_refresh_token
from backend.core.config import get_settings
from backend.models import User
from backend.schemas.auth import (
    TokenRefresh,
    TokenResponse,
    UserCreate,
    UserLogin,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])

settings = get_settings()


class SendOtpRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)


class VerifyOtpRequest(BaseModel):
    phone: str = Field(..., min_length=10, max_length=15)
    otp: str = Field(..., min_length=4, max_length=8)


# ── Email/Password auth ─────────────────────────────────────────────────────


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(db, data)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(db, data)


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: TokenRefresh, db: AsyncSession = Depends(get_db)):
    return await refresh_access_token(db, data.refresh_token)


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


# ── OTP Auth ────────────────────────────────────────────────────────────────


@router.post("/send-otp")
async def send_otp(data: SendOtpRequest, db: AsyncSession = Depends(get_db)):
    """Send OTP to phone. Phone must be registered."""
    phone = normalize_phone(data.phone)
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Phone not registered")

    otp = generate_otp()
    store_otp(data.phone, otp)
    ok, detail = await send_otp_via_gateway(data.phone, otp, settings.fast2sms_api_key)

    if not ok:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Failed to send OTP: {detail}")

    # Expose OTP in dev mode for testing
    resp: dict = {"success": True, "message": "OTP sent"}
    if settings.environment == "development":
        resp["otp"] = otp
    return resp


@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp_login(data: VerifyOtpRequest, db: AsyncSession = Depends(get_db)):
    """Verify OTP and return JWT tokens."""
    ok, detail = verify_otp(data.phone, data.otp)
    if not ok:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)

    phone = normalize_phone(data.phone)
    result = await db.execute(select(User).where(User.phone == phone))
    user = result.scalar_one_or_none()
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found or inactive")

    return TokenResponse(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
        expires_in=settings.access_token_expire_minutes * 60,
    )
