"""pytest conftest — shared fixtures for backend tests."""

import os
import sys
from pathlib import Path

import pytest

# Add project root to path so imports work
root = Path(__file__).parent.parent
sys.path.insert(0, str(root))
sys.path.insert(0, str(root.parent))  # Also add grandparent for ai_engine imports

# ── Set test environment BEFORE any backend module is imported ─────────────────
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["OPENROUTER_API_KEY"] = ""
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["ENVIRONMENT"] = "test"
os.environ["DEBUG"] = "False"

# Force settings reload so the lru_cache picks up the env overrides above
from backend.core.config import get_settings  # noqa: E402
get_settings.cache_clear()

# Force the lazy engine to rebuild with the test SQLite URL
from backend.database.session import reset_engine  # noqa: E402
reset_engine()

# ── Build a shared in-memory SQLite engine + session ──────────────────────────
# Use StaticPool so all connections share the same :memory: DB across the session.
from sqlalchemy import text, event  # noqa: E402
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine  # noqa: E402
from sqlalchemy.pool import StaticPool  # noqa: E402
from backend.database.session import Base  # noqa: E402
from backend.models import (  # noqa: E402, F401 — register all models with Base.metadata
    User, Farmer, DiseaseReport, MarketPrediction, RiskAssessment,
    YieldPrediction, IrrigationPlan, ProfitAnalysis, Feedback,
)

_test_engine = create_async_engine(
    "sqlite+aiosqlite:///:memory:",
    echo=False,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
_test_session_factory = async_sessionmaker(
    _test_engine, class_=AsyncSession, expire_on_commit=False,
)


async def _get_test_db():
    """FastAPI dependency override: yields an in-memory SQLite async session."""
    async with _test_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# ── Install dependency override on the FastAPI app ─────────────────────────────
# Must happen before TestClient is created in test_integration.py
from backend.core.dependencies import get_db  # noqa: E402
from backend.main import app  # noqa: E402

app.dependency_overrides[get_db] = _get_test_db


# ── Pytest fixtures ────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
async def clean_db():
    """Create tables fresh before each test, drop after (StaticPool = shared memory)."""
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with _test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
