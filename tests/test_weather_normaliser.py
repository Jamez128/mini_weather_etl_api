import pytest
from datetime import datetime
from pydantic import ValidationError

from app.models.raw_weather import RawWeatherInput
from app.services.weather_normalizer import normalise_weather
from app.models.location import Location

def make_raw(**overrides):
    base = dict(
        temp=86.0,
        temp_unit="Degrees Fahrenheit",
        humidity=70,
        humidity_unit="Percentage",
        wind_speed=36.0,
        wind_speed_unit="kmh",
        wind_dir="N",
        pressure=None,
        forecast_description="Thundery Showers",
        location=Location(lat=1.3521, lon=103.8198, city="Singapore", country_code="SG"),
        timestamp=datetime(2025, 12, 5, 12, 0, 0),
    )
    base.update(overrides)
    return RawWeatherInput(**base)

# ---------- Test A: happy path (conversion + feels-like) ----------

def test_normalise_weather_happy_path():
    raw = make_raw()
    out = normalise_weather(raw, source="nea")

    assert out.temperature_c == pytest.approx(30.0, rel=1e-3) # 86F -> 30C
    assert out.wind_speed_ms == pytest.approx(10.0, rel=1e-3) # 36kmh -> 10m/s
    assert out.humidity_percent == 70
    assert out.source == "nea"
    assert out.weather_text == "Thundery Showers"

# ---------- Test B: pressure passthrough stays None ----------

def test_normalise_weather_pressure_none_allowed():
    raw = make_raw(pressure=None)
    out = normalise_weather(raw, source="nea")
    assert out.pressure_hpa is None

# ---------- Test C: invalid humidity triggers model validation ----------

def test_normalise_weather_invalid_humidity_raises():
    raw = make_raw(humidity=120)
    with pytest.raises(ValidationError):
        normalise_weather(raw, source="nea")