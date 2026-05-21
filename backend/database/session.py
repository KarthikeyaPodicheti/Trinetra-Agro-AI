"""Async SQLAlchemy engine, session, and Base — Supabase PostgreSQL.

The engine and session factory are created lazily on first access so that
test environments can override DATABASE_URL before the engine is built.
"""

import ssl as _ssl
import re as _re
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase

from backend.core.config import get_settings


class Base(DeclarativeBase):
    pass


# ---------------------------------------------------------------------------
# Lazy engine / session factory — built on first access
# ---------------------------------------------------------------------------
_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker] = None  # type: ignore[type-arg]


def _build_engine() -> AsyncEngine:
    """Build an async engine from current settings (reads fresh settings each call)."""
    settings = get_settings()
    db_url = settings.database_url

    # Strip any sslmode/ssl query params — asyncpg doesn't accept them in the URL
    db_url = _re.sub(r"[?&]sslmode=[^&]*", "", db_url).rstrip("?&")
    db_url = _re.sub(r"[?&]ssl=[^&]*", "", db_url).rstrip("?&")

    if db_url.startswith("sqlite:///"):
        db_url = db_url.replace("sqlite:///", "sqlite+aiosqlite:///", 1)

    if db_url.startswith("sqlite+aiosqlite"):
        # SQLite — lightweight, no pooling
        return create_async_engine(db_url, echo=settings.debug)

    # PostgreSQL (Supabase)
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

    # Build SSL context — Supabase requires TLS
    ssl_ctx = _ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = _ssl.CERT_NONE

    return create_async_engine(
        db_url,
        echo=settings.debug,
        pool_size=5,        # Supabase Transaction Pooler: keep low
        max_overflow=10,
        pool_recycle=300,   # Recycle connections every 5 min
        connect_args={
            "ssl": ssl_ctx,
            "statement_cache_size": 0,
            "prepared_statement_cache_size": 0,
            "server_settings": {
                "search_path": "public",
                "application_name": "trinetra-agro-ai",
            },
        },
    )


def get_engine() -> AsyncEngine:
    """Return the shared engine, creating it lazily on first call."""
    global _engine
    if _engine is None:
        _engine = _build_engine()
    return _engine


def get_session_factory() -> async_sessionmaker:  # type: ignore[type-arg]
    """Return the shared session factory, creating it lazily on first call."""
    global _session_factory
    if _session_factory is None:
        _session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _session_factory


def reset_engine() -> None:
    """Force-reset the cached engine and session factory.

    Call this in test conftest.py after overriding DATABASE_URL so tests
    get a fresh engine pointed at the test database.
    """
    global _engine, _session_factory
    _engine = None
    _session_factory = None


# ---------------------------------------------------------------------------
# Module-level aliases for backwards compatibility with existing imports
# (backend.database.session.engine / backend.database.session.async_session_factory)
# ---------------------------------------------------------------------------
class _LazyEngine:
    """Proxy that delegates to get_engine() on first attribute access."""
    def __getattr__(self, name: str):
        return getattr(get_engine(), name)

    # SQLAlchemy checks `engine.dialect`, `engine.connect()` etc. directly
    async def connect(self):  # type: ignore[override]
        return await get_engine().connect()

    async def begin(self):  # type: ignore[override]
        return get_engine().begin()

    async def dispose(self):  # type: ignore[override]
        return await get_engine().dispose()


class _LazySessionFactory:
    """Proxy that delegates to get_session_factory() on call."""
    def __call__(self):
        return get_session_factory()()

    def __getattr__(self, name: str):
        return getattr(get_session_factory(), name)


engine = _LazyEngine()
async_session_factory = _LazySessionFactory()
