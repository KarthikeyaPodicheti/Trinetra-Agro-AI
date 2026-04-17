#!/usr/bin/env python3
"""Deployment health checks for Trinetra Agro AI."""

import argparse
import os
import sys
import urllib.request

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


def check_db(database_url: str) -> tuple[bool, str]:
    try:
        engine = create_engine(database_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "database connection ok"
    except Exception as exc:
        return False, f"database check failed: {exc}"


def check_http(url: str, timeout: int) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            body = response.read(200).decode("utf-8", errors="ignore").strip()
            if response.status != 200:
                return False, f"http check failed: status {response.status}"
            return True, f"http endpoint ok ({body or 'empty body'})"
    except Exception as exc:
        return False, f"http check failed: {exc}"


def default_health_url() -> str:
    port = os.getenv("PORT", "8501")
    return f"http://127.0.0.1:{port}/_stcore/health"


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Run deployment health checks")
    parser.add_argument(
        "--database-url",
        default=os.getenv("DATABASE_URL", "sqlite:///data/trinetra.db"),
        help="SQLAlchemy DATABASE_URL to test",
    )
    parser.add_argument(
        "--health-url",
        default=default_health_url(),
        help="HTTP health endpoint to test",
    )
    parser.add_argument(
        "--http-timeout",
        type=int,
        default=5,
        help="HTTP timeout in seconds",
    )
    parser.add_argument("--skip-db", action="store_true", help="Skip database check")
    parser.add_argument("--skip-http", action="store_true", help="Skip HTTP check")
    args = parser.parse_args()

    checks: list[tuple[str, bool, str]] = []

    if not args.skip_db:
        ok, msg = check_db(args.database_url)
        checks.append(("DB", ok, msg))

    if not args.skip_http:
        ok, msg = check_http(args.health_url, args.http_timeout)
        checks.append(("HTTP", ok, msg))

    if not checks:
        print("No checks selected")
        return 2

    failed = False
    for name, ok, msg in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: {msg}")
        failed = failed or (not ok)

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
