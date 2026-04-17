#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


ROOT = Path(__file__).resolve().parent


def env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def print_check(name: str, ok: bool, detail: str) -> None:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}: {detail}")


def check_required_env() -> tuple[bool, str]:
    required = ["DATABASE_URL"]
    missing = [k for k in required if not os.getenv(k, "").strip()]
    if missing:
        return False, f"missing env vars: {', '.join(missing)}"

    if env_flag("REQUIRE_LOGIN", "false") and os.getenv("AUTH_MODE", "password").strip().lower() == "otp":
        webhook = os.getenv("OTP_WEBHOOK_URL", "").strip()
        allow_dev = env_flag("OTP_ALLOW_DEV_FALLBACK", "false")
        if not webhook and not allow_dev:
            return False, "OTP mode enabled but OTP_WEBHOOK_URL missing"
        if allow_dev:
            return False, "OTP_ALLOW_DEV_FALLBACK=true is not allowed for release readiness"

    return True, "required env vars are set"


def check_db() -> tuple[bool, str]:
    db_url = os.getenv("DATABASE_URL", "")
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "database connection ok"
    except Exception as exc:
        return False, f"database check failed: {exc}"


def run_compileall() -> tuple[bool, str]:
    cmd = [sys.executable, "-m", "compileall", "app", "quick_start.py", "healthcheck.py", "otp_gateway.py", "production_runner.py"]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if proc.returncode == 0:
        return True, "compileall succeeded"
    return False, (proc.stderr or proc.stdout or "compileall failed").strip()[:500]


def run_production_check_only() -> tuple[bool, str]:
    cmd = [sys.executable, "production_runner.py", "--check-only"]
    proc = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    if proc.returncode == 0:
        return True, "production_runner check-only passed"
    return False, (proc.stderr or proc.stdout or "production check failed").strip()[:500]


def check_runner_metrics(url: str) -> tuple[bool, str]:
    try:
        r = requests.get(url, timeout=6)
        if r.status_code != 200:
            return False, f"status {r.status_code}"
        payload = r.json()
        if "app" not in payload or "last_health" not in payload:
            return False, "metrics payload missing required keys"
        return True, "metrics endpoint schema ok"
    except Exception as exc:
        return False, f"metrics check failed: {exc}"


def check_otp_webhook(url: str, token: str) -> tuple[bool, str]:
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    payload = {
        "phone": "+919999999999",
        "otp": "123456",
        "message": "Trinetra test OTP",
        "sender": "Trinetra Agro AI",
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=8)
        if 200 <= r.status_code < 300:
            return True, "otp webhook reachable"
        return False, f"otp webhook status {r.status_code}"
    except Exception as exc:
        return False, f"otp webhook check failed: {exc}"


def start_temp_runner(port: int, metrics_port: int) -> subprocess.Popen:
    cmd = [
        sys.executable,
        "production_runner.py",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--metrics-host",
        "127.0.0.1",
        "--metrics-port",
        str(metrics_port),
    ]
    return subprocess.Popen(cmd, cwd=str(ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_http_ok(url: str, timeout_sec: int = 30) -> bool:
    start = time.time()
    while time.time() - start < timeout_sec:
        try:
            r = requests.get(url, timeout=3)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(1)
    return False


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Release readiness gate")
    parser.add_argument("--skip-runner", action="store_true", help="Skip temporary runner start + metrics schema check")
    parser.add_argument("--skip-otp-webhook", action="store_true", help="Skip OTP webhook reachability check")
    parser.add_argument("--runner-port", type=int, default=18501)
    parser.add_argument("--runner-metrics-port", type=int, default=19090)
    args = parser.parse_args()

    checks = []

    checks.append(("env",) + check_required_env())
    checks.append(("database",) + check_db())
    checks.append(("compileall",) + run_compileall())
    checks.append(("production-check",) + run_production_check_only())

    runner_proc = None
    if not args.skip_runner:
        runner_proc = start_temp_runner(args.runner_port, args.runner_metrics_port)
        app_ok = wait_http_ok(f"http://127.0.0.1:{args.runner_port}/_stcore/health", timeout_sec=40)
        checks.append(("runner-app-health", app_ok, "app health reachable" if app_ok else "app health not reachable"))
        metrics_ok, metrics_detail = check_runner_metrics(f"http://127.0.0.1:{args.runner_metrics_port}/metrics")
        checks.append(("runner-metrics", metrics_ok, metrics_detail))

    if not args.skip_otp_webhook and env_flag("REQUIRE_LOGIN", "false") and os.getenv("AUTH_MODE", "password").strip().lower() == "otp":
        webhook = os.getenv("OTP_WEBHOOK_URL", "").strip()
        token = os.getenv("OTP_WEBHOOK_BEARER_TOKEN", "").strip()
        if webhook:
            checks.append(("otp-webhook",) + check_otp_webhook(webhook, token))
        else:
            checks.append(("otp-webhook", False, "OTP mode enabled but OTP_WEBHOOK_URL missing"))

    if runner_proc is not None and runner_proc.poll() is None:
        runner_proc.terminate()
        try:
            runner_proc.wait(timeout=8)
        except Exception:
            runner_proc.kill()

    failed = False
    print("\nRelease Readiness Report")
    print("-" * 28)
    for name, ok, detail in checks:
        print_check(name, ok, detail)
        failed = failed or (not ok)

    if failed:
        print("\nRelease gate failed. Fix failed checks before go-live.")
        return 1

    print("\nRelease gate passed. This build is ready for controlled deployment.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
