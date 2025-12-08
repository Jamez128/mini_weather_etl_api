import httpx
from datetime import datetime
from typing import Any

from app.models.raw_weather import RawWeatherInput, Nea24hForecastResponse
from app.services.nea_mapper import map_nea_to_raw
from app.core.config import settings

class WeatherProviderError(Exception):
    """Errors raised when calling NEA API."""

async def fetch_24h_forecast_raw() -> RawWeatherInput:
    headers = {}
    if settings.nea_api_key:
        headers["X-Api-Key"] = settings.nea_api_key
    
    async with httpx.AsyncClient(timeout=settings.nea_timeout_seconds) as client:
        try:
            resp = await client.get(settings.nea_24hr_base_url, headers=headers)
        except httpx.RequestError as exc:
            raise WeatherProviderError(f"Network error calling NEA: {exc}") from exc
    
    if resp.status_code != 200:
        raise WeatherProviderError(
            f"NEA API returned {resp.status_code}: {resp.text[:200]}"
        )
    
    # Step 1 - Convert JSON to provider specific model
    try:
        nea_model = Nea24hForecastResponse.model_validate(resp.json())
    except Exception as exc:
        raise WeatherProviderError(f"Failed to parse NEA response: {exc}") from exc
    
    # Step 2 - Convert provider model -> RawWeatherInput
    raw = map_nea_to_raw(nea_model)

    # Step 3 - Return canonical internal format
    return raw
