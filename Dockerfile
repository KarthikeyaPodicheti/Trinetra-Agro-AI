# ---- Build stage ----
FROM python:3.12-slim AS build

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime stage ----
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages from build stage
COPY --from=build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copy application code
COPY backend/ ./backend/
COPY ai_engine/ ./ai_engine/

# Expose port (Render uses $PORT)
EXPOSE 8000

# Run with CORS allowing all origins (production URL set via env var)
CMD ["sh", "-c", "python -m uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

