"""Weather router — spray advisory + hourly forecast."""

from fastapi import APIRouter, Query

from backend.schemas.weather import SprayAdvisory, WeatherForecast, WeatherHour
from backend.services.weather_service import get_forecast, spray_advisory

router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/spray-advisory", response_model=SprayAdvisory)
async def spray_check(
    lat: float = Query(default=19.07, description="Latitude"),
    lon: float = Query(default=72.87, description="Longitude"),
):
    forecast = await get_forecast(lat, lon)
    return spray_advisory(forecast)


@router.get("/forecast", response_model=WeatherForecast)
async def forecast_detail(
    lat: float = Query(default=19.07, description="Latitude"),
    lon: float = Query(default=72.87, description="Longitude"),
):
    result = await get_forecast(lat, lon)
    if "error" in result:
        return WeatherForecast(hours=[], lat=lat, lon=lon)
    return WeatherForecast(
        hours=[WeatherHour(**h) for h in result["hours"]],
        lat=result["lat"],
        lon=result["lon"],
    )
