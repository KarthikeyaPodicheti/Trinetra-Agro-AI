"""SQLAlchemy ORM models for all domain entities.

Uses JSONB for PostgreSQL (Supabase) and falls back to plain JSON for SQLite
(unit/integration tests that run against SQLite).
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    JSON,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import TypeDecorator


class FlexibleJSON(TypeDecorator):
    """Stores JSON, rendering as JSONB on PostgreSQL and JSON on SQLite.

    This lets a single ORM model work transparently in both the production
    Supabase/PostgreSQL environment and SQLite-based test environments.
    """

    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            from sqlalchemy.dialects.postgresql import JSONB
            return dialect.type_descriptor(JSONB())
        return dialect.type_descriptor(JSON())


_JsonType = FlexibleJSON

from backend.database.session import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    farmer = relationship("Farmer", back_populates="user", uselist=False, cascade="all, delete-orphan")


# ---------------------------------------------------------------------------
# Farmer profile
# ---------------------------------------------------------------------------
class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    soil_type = Column(String(50), nullable=True)
    land_size_acres = Column(Float, nullable=True)
    budget_inr = Column(Float, nullable=True)
    location = Column(String(255), nullable=True)
    crops = Column(_JsonType, nullable=True)
    irrigation_type = Column(String(50), nullable=True)
    experience_years = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
    updated_at = Column(DateTime(timezone=True), default=_utcnow, onupdate=_utcnow)

    user = relationship("User", back_populates="farmer")


# ---------------------------------------------------------------------------
# AI Feature results
# ---------------------------------------------------------------------------
class DiseaseReport(Base):
    __tablename__ = "disease_reports"

    id = Column(String(36), primary_key=True, default=_uuid)
    farmer_id = Column(String(36), ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    crop_type = Column(String(100), nullable=False)
    disease_name = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    severity = Column(String(20), nullable=True)
    image_path = Column(String(500), nullable=True)
    treatment = Column(Text, nullable=True)
    prevention_tips = Column(_JsonType, nullable=True)
    analysis_details = Column(_JsonType, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class MarketPrediction(Base):
    __tablename__ = "market_predictions"

    id = Column(String(36), primary_key=True, default=_uuid)
    farmer_id = Column(String(36), ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    crop = Column(String(100), nullable=False)
    location = Column(String(255), nullable=True)
    forecast_days = Column(Integer, nullable=False)
    current_price = Column(Float, nullable=True)
    trend = Column(String(20), nullable=True)
    recommendation_action = Column(String(20), nullable=True)
    predictions_json = Column(_JsonType, nullable=True)
    data_source = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(String(36), primary_key=True, default=_uuid)
    farmer_id = Column(String(36), ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    crop = Column(String(100), nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=False)
    breakdown_json = Column(_JsonType, nullable=True)
    factors = Column(_JsonType, nullable=True)
    mitigations = Column(_JsonType, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class YieldPrediction(Base):
    __tablename__ = "yield_predictions"

    id = Column(String(36), primary_key=True, default=_uuid)
    farmer_id = Column(String(36), ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    crop = Column(String(100), nullable=False)
    land_size_acres = Column(Float, nullable=False)
    soil_type = Column(String(50), nullable=True)
    irrigation = Column(Boolean, default=True)
    estimate_conservative = Column(Float, nullable=True)
    estimate_moderate = Column(Float, nullable=True)
    estimate_optimistic = Column(Float, nullable=True)
    unit = Column(String(20), nullable=True)
    multipliers_json = Column(_JsonType, nullable=True)
    season = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class IrrigationPlan(Base):
    __tablename__ = "irrigation_plans"

    id = Column(String(36), primary_key=True, default=_uuid)
    farmer_id = Column(String(36), ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    crop = Column(String(100), nullable=False)
    land_size_acres = Column(Float, nullable=False)
    growth_stage = Column(String(50), nullable=True)
    daily_litres = Column(Float, nullable=True)
    weekly_litres = Column(Float, nullable=True)
    method = Column(String(100), nullable=True)
    schedule_json = Column(_JsonType, nullable=True)
    tips = Column(_JsonType, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class ProfitAnalysis(Base):
    __tablename__ = "profit_analyses"

    id = Column(String(36), primary_key=True, default=_uuid)
    farmer_id = Column(String(36), ForeignKey("farmers.id", ondelete="SET NULL"), nullable=True)
    crop = Column(String(100), nullable=False)
    land_size_acres = Column(Float, nullable=False)
    irrigation = Column(Boolean, default=True)
    cost_total = Column(Float, nullable=True)
    cost_per_acre = Column(Float, nullable=True)
    cost_breakdown_json = Column(_JsonType, nullable=True)
    profit_conservative = Column(Float, nullable=True)
    profit_moderate = Column(Float, nullable=True)
    profit_optimistic = Column(Float, nullable=True)
    roi_conservative = Column(Float, nullable=True)
    roi_moderate = Column(Float, nullable=True)
    roi_optimistic = Column(Float, nullable=True)
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(String(36), primary_key=True, default=_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    feature = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=_utcnow)
