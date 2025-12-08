import json
from pathlib import Path

import pytest
import respx
from httpx import Response

from app.services.weather_provider import fetch_24h_forecast_raw
from app.core.config import settings

@pytest.mark.asyncio
@respx.mock
async def test_fetch_24h_forecast_raw_happy_path():
    # Arrange: load sample JSON and mock NEA endpoint
    sample_path = Path("provider_sample_response.json")
    raw_json = json.loads(sample_path.read_text())

    # Mock the GET request to NEA URL
    respx.get(settings.nea_24hr_base_url).mock(
        return_value=Response(200, json=raw_json)
    )

    # Act: call the provider function
    raw = await fetch_24h_forecast_raw()

    # Assert: basic sanity checks
    assert raw.temp is not None
    assert raw.humidity is not None
    assert raw.wind_speed is not None

    # You can be stricter if you like, similar to the mapper test:
    # e.g., re-validate raw_json -> Nea24hForecastResponse and compare ranges


@pytest.mark.asyncio
@respx.mock
async def test_fetch_24h_forecast_raw_non_200_raises():
    # Arrange: NEA returns an error
    respx.get(settings.nea_24hr_base_url).mock(
        return_value=Response(500, json={"error": "server error"})
    )

    # Act & Assert: your WeatherProviderError should be raised
    from app.services.weather_provider import WeatherProviderError

    with pytest.raises(WeatherProviderError):
        await fetch_24h_forecast_raw()


@pytest.mark.asyncio
@respx.mock
async def test_fetch_24h_forecast_network_error():
    import httpx
    from app.services.weather_provider import WeatherProviderError

    respx.get(settings.nea_24hr_base_url).mock(side_effect=httpx.ConnectTimeout("Timeout"))

    with pytest.raises(WeatherProviderError):
        await fetch_24h_forecast_raw()
