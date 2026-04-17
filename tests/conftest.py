import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def pytest_runtest_setup():
    os.environ.setdefault("OPENROUTER_API_KEY", "")
    os.environ.setdefault("MARKET_DATA_API_KEY", "")
