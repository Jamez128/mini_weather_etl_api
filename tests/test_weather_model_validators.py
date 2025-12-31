import pytest

from pydantic import ValidationError

from app.models.weather import NormalisedWeather
from app.models.location import Location

def make_valid_weather(**overrides):
    base = dict(
        location=Location(lat=1.3521, lon=103.8198, city="Singapore", country_code="SG"),
        timestamp_utc="2025-12-05T12:00:00Z",
        temperature_c=30.0,
        feels_like_c=33.0,
        humidity_percent=70,
        wind_speed_ms=3.2,
        wind_direction="N",
        pressure_hpa=1007.0,
        weather_code="TL",
        weather_text="Thundery Showers",
        source="nea",
    )
    base.update(overrides)
    return NormalisedWeather(**base)

# ---------- test 1: invalid humidity raises validation error ----------

def test_normalised_weather_invalid_humidity_raises():
    with pytest.raises(ValidationError) as exc:
        make_valid_weather(humidity_percent=120)
    
    # Optional: assert the error mentions the field
    assert "humidity_percent" in str(exc.value)

# ---------- test 2: invalid temperature raises validation error ----------

def test_normalised_weather_invalid_temperature_raises():
    with pytest.raises(ValidationError) as exc:
        make_valid_weather(temperature_c=100.0)
    
    assert "temperature_c" in str(exc.value)

# ---------- test 3: would be pressure range (pressure not in nea), 
# can add if alternative external APIs are incorporated in the future