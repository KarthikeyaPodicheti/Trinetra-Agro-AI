FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN mkdir -p data logs

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=6s --start-period=30s --retries=3 \
  CMD python -c "import os,urllib.request; port=os.getenv('PORT','8501'); urllib.request.urlopen(f'http://127.0.0.1:{port}/_stcore/health', timeout=5)"

CMD ["sh", "-c", "streamlit run app/main.py --server.headless=true --server.address=0.0.0.0 --server.port=${PORT:-8501}"]
