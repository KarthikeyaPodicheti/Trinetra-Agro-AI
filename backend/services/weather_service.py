"""Weather service — Open-Meteo API (free, no key required)."""

import time
from typing import Any, Dict, List, Optional

import httpx

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

# Simple cache — 15 minute TTL
_cache: Dict[str, Dict[str, Any]] = {}
CACHE_TTL = 900


async def get_forecast(lat: float, lon: float) -> Dict[str, Any]:
    """Fetch 48-hour hourly forecast from Open-Meteo."""
    cache_key = f"{lat:.2f}:{lon:.2f}"
    now = time.time()
    if cache_key in _cache and (now - _cache[cache_key]["ts"]) < CACHE_TTL:
        return _cache[cache_key]["data"]

    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "forecast_days": 2,
        "timezone": "auto",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(OPEN_METEO_URL, params=params)
            data = resp.json()
    except Exception:
        if cache_key in _cache:
            return _cache[cache_key]["data"]
        return {"error": "Weather service unavailable"}

    hourly = data.get("hourly", {})
    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    precip = hourly.get("precipitation", [])
    winds = hourly.get("wind_speed_10m", [])

    hours = []
    for i in range(min(len(times), 48)):
        hours.append({
            "time": times[i],
            "temp_c": temps[i] if i < len(temps) else 0,
            "rain_mm": precip[i] if i < len(precip) else 0,
            "wind_kmh": winds[i] if i < len(winds) else 0,
        })

    result = {"hours": hours, "lat": lat, "lon": lon}
    _cache[cache_key] = {"ts": now, "data": result}
    return result


def spray_advisory(forecast: Dict[str, Any]) -> Dict[str, Any]:
    """Apply spray rules to forecast and return recommendation."""
    hours = forecast.get("hours", [])
    if not hours:
        return {"can_spray": False, "reason": "No forecast data available", "next_safe_window": None}

    # Check next 24 hours
    next_24 = hours[:24]

    # Rule 1: Rain in next 6 hours
    for h in next_24[:6]:
        if h["rain_mm"] > 0.5:
            return {
                "can_spray": False,
                "reason": f"Rain ({h['rain_mm']:.1f}mm) expected at {h['time']}. Spray will wash off.",
                "next_rain": h["time"],
                "next_safe_window": _find_safe_window(next_24),
            }

    # Rule 2: High wind
    for h in next_24[:12]:
        if h["wind_kmh"] > 15:
            return {
                "can_spray": False,
                "reason": f"Wind speed {h['wind_kmh']:.0f} km/h at {h['time']} — spray will drift.",
                "next_safe_window": _find_safe_window(next_24),
            }

    # Rule 3: High temperature
    for h in next_24[:12]:
        if h["temp_c"] > 35:
            return {
                "can_spray": False,
                "reason": f"Temperature {h['temp_c']:.0f}°C at {h['time']} — chemicals evaporate too fast.",
                "next_safe_window": _find_safe_window(next_24),
            }

    # All clear — find next safe window
    next_rain = None
    for h in next_24:
        if h["rain_mm"] > 0.5:
            next_rain = h["time"]
            break

    return {
        "can_spray": True,
        "reason": "No rain, low wind, moderate temperature — safe to spray.",
        "next_rain": next_rain,
        "next_safe_window": _find_safe_window(next_24),
    }


def _find_safe_window(hours: List[Dict]) -> Optional[str]:
    """Find next 3-hour block with no rain and low wind."""
    for i in range(len(hours) - 3):
        block = hours[i:i+3]
        if all(h["rain_mm"] < 0.5 for h in block) and all(h["wind_kmh"] <= 15 for h in block):
            return f"{block[0]['time']} to {block[-1]['time']}"
    return None
