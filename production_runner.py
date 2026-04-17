#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

import requests
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


ROOT = Path(__file__).resolve().parent
LOG_DIR = ROOT / "logs"
LOG_MAX_BYTES = int(os.getenv("RUNNER_LOG_MAX_BYTES", str(5 * 1024 * 1024)))
LOG_BACKUP_COUNT = int(os.getenv("RUNNER_LOG_BACKUP_COUNT", "5"))


def env_flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}


def check_required_env() -> list[str]:
    missing = []
    if not os.getenv("DATABASE_URL", "").strip():
        missing.append("DATABASE_URL")

    if env_flag("REQUIRE_LOGIN", "false") and os.getenv("AUTH_MODE", "password").strip().lower() == "otp":
        if not os.getenv("OTP_WEBHOOK_URL", "").strip() and not env_flag("OTP_ALLOW_DEV_FALLBACK", "false"):
            missing.append("OTP_WEBHOOK_URL (or set OTP_ALLOW_DEV_FALLBACK=true for local testing only)")

    return missing


def check_db(database_url: str) -> tuple[bool, str]:
    try:
        engine = create_engine(database_url, pool_pre_ping=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True, "database ok"
    except Exception as exc:
        return False, f"database check failed: {exc}"


def check_http(url: str, timeout: int = 6) -> tuple[bool, str]:
    try:
        r = requests.get(url, timeout=timeout)
        if r.status_code == 200:
            return True, "http ok"
        return False, f"http status {r.status_code}"
    except Exception as exc:
        return False, f"http check failed: {exc}"


def start_process(command: list[str], log_file: Path) -> subprocess.Popen:
    rotate_logs(log_file, max_bytes=LOG_MAX_BYTES, backups=LOG_BACKUP_COUNT)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    fh = open(log_file, "a", encoding="utf-8")
    return subprocess.Popen(command, cwd=str(ROOT), stdout=fh, stderr=fh)


def rotate_logs(log_file: Path, max_bytes: int, backups: int) -> None:
    try:
        if not log_file.exists() or log_file.stat().st_size < max_bytes:
            return
        oldest = log_file.with_name(f"{log_file.name}.{backups}")
        if oldest.exists():
            oldest.unlink()
        for idx in range(backups - 1, 0, -1):
            src = log_file.with_name(f"{log_file.name}.{idx}")
            dst = log_file.with_name(f"{log_file.name}.{idx + 1}")
            if src.exists():
                src.replace(dst)
        log_file.replace(log_file.with_name(f"{log_file.name}.1"))
    except Exception:
        pass


def prune_old_logs(log_dir: Path, keep_days: int = 7) -> None:
    try:
        now = time.time()
        threshold = now - (keep_days * 24 * 60 * 60)
        if not log_dir.exists():
            return
        for path in log_dir.glob("*.log*"):
            if path.is_file() and path.stat().st_mtime < threshold:
                path.unlink()
    except Exception:
        pass


class MetricsServer:
    def __init__(self, host: str, port: int, status_ref: dict):
        self.host = host
        self.port = port
        self.status_ref = status_ref
        self._server = None
        self._thread = None

    def start(self) -> None:
        status_ref = self.status_ref

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):  # noqa: N802
                if self.path not in {"/metrics", "/healthz"}:
                    self.send_response(404)
                    self.end_headers()
                    return
                payload = json.dumps(status_ref).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)

            def log_message(self, _format, *_args):
                return

        self._server = HTTPServer((self.host, self.port), Handler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if self._server:
            self._server.shutdown()
            self._server.server_close()


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description="Production startup runner")
    parser.add_argument("--host", default=os.getenv("APP_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("PORT", "8501")))
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--start-gateway", action="store_true")
    parser.add_argument("--gateway-host", default=os.getenv("OTP_GATEWAY_HOST", "127.0.0.1"))
    parser.add_argument("--gateway-port", type=int, default=int(os.getenv("OTP_GATEWAY_PORT", "8081")))
    parser.add_argument("--metrics-host", default=os.getenv("RUNNER_METRICS_HOST", "127.0.0.1"))
    parser.add_argument("--metrics-port", type=int, default=int(os.getenv("RUNNER_METRICS_PORT", "9090")))
    args = parser.parse_args()

    prune_old_logs(LOG_DIR, keep_days=int(os.getenv("RUNNER_LOG_RETENTION_DAYS", "7")))

    missing = check_required_env()
    if missing:
        print("Missing required configuration:")
        for m in missing:
            print(f"- {m}")
        return 2

    db_url = os.getenv("DATABASE_URL", "")
    ok_db, msg_db = check_db(db_url)
    print(f"[{'PASS' if ok_db else 'FAIL'}] DB: {msg_db}")
    if not ok_db:
        return 1

    if args.check_only:
        print("Configuration and DB checks passed.")
        return 0

    procs: list[subprocess.Popen] = []
    status = {
        "runner_started_at": int(time.time()),
        "app": {"running": False, "pid": None},
        "otp_gateway": {"running": False, "pid": None},
        "last_health": {"ok": False, "checked_at": None},
    }
    metrics = MetricsServer(args.metrics_host, args.metrics_port, status)
    metrics.start()
    print(f"Metrics endpoint: http://{args.metrics_host}:{args.metrics_port}/metrics")
    otp_mode = env_flag("REQUIRE_LOGIN", "false") and os.getenv("AUTH_MODE", "password").strip().lower() == "otp"
    gateway_needed = args.start_gateway or (otp_mode and "127.0.0.1" in os.getenv("OTP_WEBHOOK_URL", ""))

    if gateway_needed:
        gateway_log = LOG_DIR / "otp-gateway.log"
        p = start_process(
            [sys.executable, "otp_gateway.py", "--host", args.gateway_host, "--port", str(args.gateway_port)],
            gateway_log,
        )
        procs.append(p)
        print(f"Started OTP gateway (pid={p.pid}), log={gateway_log}")
        status["otp_gateway"] = {"running": True, "pid": p.pid}
        time.sleep(2)

    app_log = LOG_DIR / "app-production.log"
    app_cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app/main.py",
        "--server.headless=true",
        f"--server.address={args.host}",
        f"--server.port={args.port}",
    ]
    app_proc = start_process(app_cmd, app_log)
    procs.append(app_proc)
    print(f"Started app (pid={app_proc.pid}), log={app_log}")
    status["app"] = {"running": True, "pid": app_proc.pid}

    health_url = f"http://127.0.0.1:{args.port}/_stcore/health"
    passed = False
    for _ in range(20):
        time.sleep(1)
        ok_http, _ = check_http(health_url)
        status["last_health"] = {"ok": ok_http, "checked_at": int(time.time())}
        if ok_http:
            passed = True
            break

    if not passed:
        print("[FAIL] App health check failed after startup.")
        for p in procs:
            if p.poll() is None:
                p.terminate()
        metrics.stop()
        return 1

    print("[PASS] App health check passed.")
    print("Press Ctrl+C to stop all services.")

    def _shutdown(*_args) -> None:
        print("Shutting down services...")
        status["app"]["running"] = False
        status["otp_gateway"]["running"] = False
        for p in reversed(procs):
            if p.poll() is None:
                p.terminate()
        time.sleep(2)
        for p in reversed(procs):
            if p.poll() is None:
                p.kill()
        metrics.stop()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, _shutdown)
    signal.signal(signal.SIGTERM, _shutdown)

    while True:
        time.sleep(1)
        if app_proc.poll() is not None:
            print("App process exited. Stopping all services.")
            _shutdown()


if __name__ == "__main__":
    sys.exit(main())
