"""External data source adapters with graceful fallback behavior."""

from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
DATA_GOV_MARKET_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def fetch_weather(location: str, api_key: Optional[str] = None, timeout: int = 8) -> Dict[str, Any]:
    key = (api_key or os.getenv("WEATHER_API_KEY", "")).strip()
    if not key:
        return {
            "success": False,
            "error": "WEATHER_API_KEY not configured",
            "source": "fallback",
            "updated_at": _now_iso(),
        }

    try:
        resp = requests.get(
            OPENWEATHER_URL,
            params={"q": location, "appid": key, "units": "metric"},
            timeout=timeout,
        )
        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"weather API status {resp.status_code}",
                "source": "fallback",
                "updated_at": _now_iso(),
            }

        payload = resp.json()
        main = payload.get("main", {})
        wind = payload.get("wind", {})
        weather = (payload.get("weather") or [{}])[0]
        desc = str(weather.get("description", "")).lower()
        rain_mm = 0.0
        rain_data = payload.get("rain", {})
        if isinstance(rain_data, dict):
            rain_mm = float(rain_data.get("1h") or rain_data.get("3h") or 0.0)

        if rain_mm >= 15 or "heavy" in desc:
            rainfall_forecast = "Heavy rain"
        elif rain_mm >= 5 or "moderate" in desc:
            rainfall_forecast = "Moderate rain"
        elif rain_mm > 0 or "rain" in desc or "drizzle" in desc:
            rainfall_forecast = "Light rain"
        else:
            rainfall_forecast = "No rain"

        return {
            "success": True,
            "source": "openweathermap",
            "updated_at": _now_iso(),
            "location": payload.get("name") or location,
            "temperature": main.get("temp"),
            "humidity": main.get("humidity"),
            "rainfall_forecast": rainfall_forecast,
            "wind_speed": wind.get("speed"),
            "uv_index": None,
            "description": weather.get("description", ""),
        }
    except Exception as exc:
        return {
            "success": False,
            "error": f"weather API error: {exc}",
            "source": "fallback",
            "updated_at": _now_iso(),
        }


def fetch_mandi_prices(
    crop: str,
    location: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 8,
    limit: int = 25,
) -> Dict[str, Any]:
    key = (api_key or os.getenv("MARKET_DATA_API_KEY", "")).strip()
    if not key:
        return {
            "success": False,
            "error": "MARKET_DATA_API_KEY not configured",
            "source": "fallback",
            "updated_at": _now_iso(),
        }

    commodity = crop.strip().title()
    try:
        params = {
            "api-key": key,
            "format": "json",
            "limit": limit,
            "filters[commodity]": commodity,
        }
        if location:
            params["filters[market]"] = location.strip().title()

        resp = requests.get(DATA_GOV_MARKET_URL, params=params, timeout=timeout)
        if resp.status_code != 200:
            return {
                "success": False,
                "error": f"market API status {resp.status_code}",
                "source": "fallback",
                "updated_at": _now_iso(),
            }

        payload = resp.json()
        records = payload.get("records") or []
        prices = []
        markets = set()
        states = set()
        for row in records:
            market_name = row.get("market")
            state_name = row.get("state")
            if market_name:
                markets.add(str(market_name))
            if state_name:
                states.add(str(state_name))

            modal = row.get("modal_price")
            if modal is None:
                continue
            try:
                prices.append(float(str(modal).replace(",", "")))
            except Exception:
                continue

        if not prices:
            return {
                "success": False,
                "error": "no usable modal_price records from API",
                "source": "fallback",
                "updated_at": _now_iso(),
            }

        current = sum(prices) / len(prices)
        return {
            "success": True,
            "source": "data.gov.in",
            "updated_at": _now_iso(),
            "commodity": commodity,
            "current_price": round(current, 2),
            "currency": "₹/quintal",
            "records_used": len(prices),
            "markets": sorted(markets)[:10],
            "states": sorted(states)[:10],
        }
    except Exception as exc:
        return {
            "success": False,
            "error": f"market API error: {exc}",
            "source": "fallback",
            "updated_at": _now_iso(),
        }
