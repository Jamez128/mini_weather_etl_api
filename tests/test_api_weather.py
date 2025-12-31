# import pytest
from datetime import datetime
from fastapi.testclient import TestClient

from app.main import app
from app.models.location import Location
from app.models.raw_weather import RawWeatherInput

client = TestClient(app)

def make_raw(**overrides) -> RawWeatherInput:
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
        timestamp=datetime(2025, 12, 5, 12, 0, 0)
    )
    base.update(overrides)
    return RawWeatherInput(**base)

def test_get_weather_current_happy_path(monkeypatch):
    # IMPORTANT: patch where the function is *used* (app.api.weather),
    # where imported fetch_24h_forecast_raw into that module
    async def fake_fetch():
        return make_raw()
    
    monkeypatch.setattr("app.api.weather.fetch_24h_forecast_raw", fake_fetch)

    r = client.get("/weather/current")
    assert r.status_code == 200

    body = r.json()
    assert body["source"] == "nea"
    assert body["humidity_percent"] == 70
    assert body["weather_text"] == "Thundery Showers"
    
    # basic conversion sanity checks
    assert abs(body["temperature_c"] -30.0) < 0.2 # 86F -> 30C
    assert abs(body["wind_speed_ms"] -10.0) < 0.3 # 36kmh -> 10m/s

def test_post_weather_normalise_happy_path():
    raw = make_raw()

    # send dict/json, not the model object
    r = client.post("/weather/normalise", json=raw.model_dump(mode="json"))
    assert r.status_code == 200

    body = r.json()
    assert body["source"] == "client"
    assert body["weather_text"] == "Thundery Showers"
    assert abs(body["temperature_c"] -30.0) < 0.2

def test_post_weather_normalise_invalid_humidity_returns_422():
    raw = make_raw(humidity=120)
    r = client.post("/weather/normalise", json=raw.model_dump(mode="json"))

    assert r.status_code == 422
    body =r.json()
    assert "detail" in body
    assert isinstance(body["detail"], list)
    assert any((err.get("loc") or [])[-1] == "humidity_percent" for err in body["detail"])

def test_post_weather_normalise_unsupported_unit_returns_400():
    raw = make_raw(humidity_unit="foo")
    r = client.post("/weather/normalise", json=raw.model_dump(mode="json"))

    assert r.status_code == 400
    assert "Unsupported humidity unit" in r.json()["detail"]