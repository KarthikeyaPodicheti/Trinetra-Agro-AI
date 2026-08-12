"""Shared pytest fixtures.

Runs the FastAPI app against a throwaway SQLite database (via the project's
existing sqlite+aiosqlite support in database/session.py) — no Postgres, no
network, no real credentials.
"""

import asyncio
import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

_extra = os.environ.get("PYTEST_XDIST_WORKER", "")
TEST_DB_PATH = Path(tempfile.gettempdir()) / f"trinetra_test_{_extra}.db"

os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_PATH}"
os.environ["ENVIRONMENT"] = "development"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"

import pytest

from backend.core.config import get_settings

get_settings.cache_clear()

from fastapi.testclient import TestClient

import backend.models  # noqa: F401  (register every table on Base.metadata)
from backend.database.session import Base, get_engine, reset_engine
from backend.main import app


def _create_schema() -> None:
    async def _go() -> None:
        async with get_engine().begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(_go())


@pytest.fixture(scope="session", autouse=True)
def _db():
    reset_engine()
    _create_schema()
    yield
    asyncio.run(get_engine().dispose())
    reset_engine()
    if TEST_DB_PATH.exists():
        TEST_DB_PATH.unlink()


@pytest.fixture(scope="session")
def client(_db):
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def _no_otp_stale():
    from backend.auth import otp_service

    otp_service._otp_store.clear()
    yield
    otp_service._otp_store.clear()