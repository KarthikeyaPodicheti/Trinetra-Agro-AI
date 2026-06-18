"""Weather schemas."""

from typing import Optional, List
from pydantic import BaseModel


class WeatherHour(BaseModel):
    time: str
    temp_c: float
    rain_mm: float
    wind_kmh: float


class WeatherForecast(BaseModel):
    hours: List[WeatherHour]
    lat: float
    lon: float


class SprayAdvisory(BaseModel):
    can_spray: bool
    reason: str
    next_rain: Optional[str] = None
    next_safe_window: Optional[str] = None
