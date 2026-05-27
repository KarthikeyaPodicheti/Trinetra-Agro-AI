"""Trinetra Agro AI — FastAPI application entry point.

Schema is managed by Supabase migrations (supabase/migrations/).
Tables are NOT auto-created on startup — run `npx supabase db push` instead.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.auth.router import router as auth_router
from backend.routers.ai_features import router as ai_router
from backend.routers.chatbot import router as chatbot_router
from backend.routers.disease import router as disease_router
from backend.routers.feedback import router as feedback_router
from backend.routers.profile import router as profile_router
from backend.core.config import get_settings
from backend.database.session import get_engine
from backend.middleware.logging import LoggingMiddleware

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Startup: validate DB connectivity. Shutdown: dispose connection pool.

    Tables are managed by Supabase migrations — no auto-create here.
    """
    import sqlalchemy
    eng = get_engine()
    async with eng.connect() as conn:
        await conn.execute(sqlalchemy.text("SELECT 1"))
    yield
    await eng.dispose()


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    docs_url="/docs",   # Always expose docs (Supabase is production-grade)
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Middleware — order matters: outermost first
app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(ai_router)
app.include_router(chatbot_router)
app.include_router(disease_router)
app.include_router(feedback_router)
app.include_router(profile_router)


@app.get("/health", tags=["system"])
async def health_check():
    return {
        "status": "healthy",
        "version": settings.version,
        "environment": settings.environment,
        "database": "supabase_postgresql",
    }


@app.get("/", tags=["system"])
async def root():
    return {
        "app": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
        "health": "/health",
    }
