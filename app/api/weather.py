from pydantic import ValidationError

from fastapi import APIRouter, Body

from app.models.raw_weather import RawWeatherInput
from app.models.weather import NormalisedWeather
from app.services.weather_normalizer import normalise_weather
from app.services.weather_provider import fetch_24h_forecast_raw

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/current", response_model=NormalisedWeather)
async def get_current_weather() -> NormalisedWeather:
    raw = await fetch_24h_forecast_raw()
    return normalise_weather(raw, source="nea")

@router.post("/normalise", response_model=NormalisedWeather)
def normalise_payload(payload: RawWeatherInput = Body(...)) -> NormalisedWeather:
    return normalise_weather(payload, source="client")
    