"""
Database module for Trinetra Agro AI
SQLite + SQLAlchemy persistence layer
"""

import os
from datetime import datetime
from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, Float, String, Text, DateTime, Boolean, func
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

# --------------- setup ---------------
PROJECT_ROOT = Path(__file__).parent.parent.parent
DEFAULT_SQLITE_PATH = PROJECT_ROOT / "data" / "trinetra.db"
DEFAULT_SQLITE_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}")

if DATABASE_URL.startswith("sqlite:///"):
    sqlite_target = DATABASE_URL.replace("sqlite:///", "", 1)
    sqlite_path = Path(sqlite_target)
    if not sqlite_path.is_absolute():
        sqlite_path = PROJECT_ROOT / sqlite_path
    sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    DATABASE_URL = f"sqlite:///{sqlite_path.as_posix()}"
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False},
    )
else:
    engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# --------------- models ---------------

class Farmer(Base):
    __tablename__ = "farmers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), default="")
    land_size = Column(Float, default=1.0)
    soil_type = Column(String(60), default="")
    budget = Column(Float, default=50000)
    location = Column(String(120), default="")
    language = Column(String(30), default="English")
    created_at = Column(DateTime, default=datetime.utcnow)


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    farmer_id = Column(Integer, default=0)
    role = Column(String(20))          # "user" or "bot"
    message = Column(Text)
    intent = Column(String(40), default="")
    created_at = Column(DateTime, default=datetime.utcnow)


class DiseaseDetection(Base):
    __tablename__ = "disease_detections"

    id = Column(Integer, primary_key=True, autoincrement=True)
    farmer_id = Column(Integer, default=0)
    crop_type = Column(String(40))
    disease = Column(String(120))
    confidence = Column(Float)
    severity = Column(String(60))
    created_at = Column(DateTime, default=datetime.utcnow)


class MarketQuery(Base):
    __tablename__ = "market_queries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    farmer_id = Column(Integer, default=0)
    crop = Column(String(40))
    current_price = Column(Float)
    trend = Column(String(30))
    recommendation = Column(String(30))
    created_at = Column(DateTime, default=datetime.utcnow)


class CropRecommendation(Base):
    __tablename__ = "crop_recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    farmer_id = Column(Integer, default=0)
    recommended_crops = Column(Text)    # JSON string
    risk_level = Column(String(20))
    created_at = Column(DateTime, default=datetime.utcnow)


class EventLog(Base):
    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(80), default="")
    status = Column(String(20), default="ok")
    details = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)


# --------------- create tables ---------------
Base.metadata.create_all(engine)


# --------------- helpers ---------------

def get_session():
    """Return a new DB session (caller must close)."""
    return SessionLocal()


def save_farmer(name: str, land_size: float, soil_type: str,
                budget: float, location: str, language: str = "English") -> int:
    """Insert or update farmer, return farmer id."""
    session = SessionLocal()
    try:
        farmer = Farmer(
            name=name, land_size=land_size, soil_type=soil_type,
            budget=budget, location=location, language=language
        )
        session.add(farmer)
        session.commit()
        fid = farmer.id
        return fid
    finally:
        session.close()


def save_conversation(farmer_id: int, role: str, message: str, intent: str = ""):
    session = SessionLocal()
    try:
        session.add(Conversation(farmer_id=farmer_id, role=role,
                                 message=message, intent=intent))
        session.commit()
    finally:
        session.close()


def save_disease_detection(farmer_id: int, crop_type: str, disease: str,
                           confidence: float, severity: str):
    session = SessionLocal()
    try:
        session.add(DiseaseDetection(
            farmer_id=farmer_id, crop_type=crop_type, disease=disease,
            confidence=confidence, severity=severity
        ))
        session.commit()
    finally:
        session.close()


def save_market_query(farmer_id: int, crop: str, current_price: float,
                      trend: str, recommendation: str):
    session = SessionLocal()
    try:
        session.add(MarketQuery(
            farmer_id=farmer_id, crop=crop, current_price=current_price,
            trend=trend, recommendation=recommendation
        ))
        session.commit()
    finally:
        session.close()


def save_crop_recommendation(farmer_id: int, recommended_crops: str,
                             risk_level: str):
    session = SessionLocal()
    try:
        session.add(CropRecommendation(
            farmer_id=farmer_id, recommended_crops=recommended_crops,
            risk_level=risk_level
        ))
        session.commit()
    finally:
        session.close()


def get_recent_conversations(farmer_id: int, limit: int = 50):
    session = SessionLocal()
    try:
        rows = (session.query(Conversation)
                .filter(Conversation.farmer_id == farmer_id)
                .order_by(Conversation.id.desc())
                .limit(limit).all())
        return list(reversed(rows))
    finally:
        session.close()


def save_event(event_type: str, status: str = "ok", details: str = ""):
    session = SessionLocal()
    try:
        session.add(EventLog(event_type=event_type[:80], status=status[:20], details=(details or "")[:2000]))
        session.commit()
    finally:
        session.close()


def get_event_counts(days: int = 7):
    session = SessionLocal()
    try:
        cutoff = datetime.utcnow()
        if days and days > 0:
            from datetime import timedelta
            cutoff = datetime.utcnow() - timedelta(days=days)

        rows = (
            session.query(EventLog.event_type, EventLog.status, func.count(EventLog.id))
            .filter(EventLog.created_at >= cutoff)
            .group_by(EventLog.event_type, EventLog.status)
            .all()
        )
        counts = {}
        for event_type, status, count in rows:
            if event_type not in counts:
                counts[event_type] = {"ok": 0, "error": 0, "other": 0}
            if status == "ok":
                counts[event_type]["ok"] += int(count)
            elif status == "error":
                counts[event_type]["error"] += int(count)
            else:
                counts[event_type]["other"] += int(count)
        return counts
    finally:
        session.close()


def get_recent_events(limit: int = 50):
    session = SessionLocal()
    try:
        rows = (
            session.query(EventLog)
            .order_by(EventLog.id.desc())
            .limit(limit)
            .all()
        )
        return list(rows)
    finally:
        session.close()
