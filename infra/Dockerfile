# syntax=docker/dockerfile:1
FROM python:3.9-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# Backend dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 && rm -rf /var/lib/apt/lists/*

# Backend layer
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/ ./backend/

# AI engine layer
COPY ai_engine/ ./ai_engine/

# Data directory
RUN mkdir -p data

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

# ---------- Frontend (multi-stage) ----------
FROM base AS frontend
RUN pip install --no-cache-dir streamlit httpx plotly
COPY frontend/ ./frontend/
EXPOSE 8501
CMD ["streamlit", "run", "frontend/app.py", "--server.port", "8501", "--server.headless", "true"]
