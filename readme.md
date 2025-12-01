1. High-Level Product Description

A FastAPI microservice that fetches weather data from a 3rd-party API, normalises it into a clean internal schema, and exposes it through a simple, predictable API for downstream services or analytics.

Core responsibilities

Fetch raw weather data from a configurable external API

Normalise fields:

Units (°C vs °F, m/s vs km/h, etc.)

Naming (API-specific → standard internal naming)

Validate value ranges and required fields using Pydantic

Expose endpoints for:

Current weather at a location

Normalisation of arbitrary raw payloads (for later ML pipelines)

Handle errors gracefully and consistently

2. Non-Functional Goals (Engineering Focus)

You want to hit your Week 1–4 bullets:

Python OOP, modules, error handling ✅

PEP8, typing, docstrings, clean patterns ✅

Pydantic v2 schemas ✅

pytest unit tests (fixtures, mocks) ✅

Docker basics + project structure ✅

Git workflow ✅

So the spec will be slightly “over-engineered” compared to a toy project — on purpose.

3. API Design

Base path assumption: /api/v1

3.1 Health Endpoints (tiny but realistic)

You’ll reuse this pattern in every future service.

GET /health/live

Purpose: “Is the process up?”

Response (200):

{ "status": "ok" }

GET /health/ready

Purpose: “Is the service ready to serve traffic?”

For MVP:

Option A: always returns ready.

Option B (nicer): periodically check last successful call to external provider.

Response:

{
  "status": "ready",
  "details": {
    "external_weather_api_reachable": true
  }
}

3.2 Current Weather Endpoint (Fetch + Normalise)
GET /weather/current

Query params (Pydantic-validated via dependency):

Option 1 (city-based):

city: str

country_code: str | None = "SG"

Option 2 (lat/lon-based, nicer for future ML):

lat: float

lon: float

Pick the one you prefer, or support both.

Process:

Validate location input.

Call external API (with timeout).

Receive raw JSON.

Convert raw JSON → RawWeatherReading Pydantic model (strict).

Convert RawWeatherReading → NormalizedWeather model.

Return NormalizedWeather as JSON.

NormalizedWeather schema (example):

{
  "location": {
    "lat": 1.3521,
    "lon": 103.8198,
    "city": "Singapore",
    "country_code": "SG"
  },
  "timestamp_utc": "2025-12-01T12:15:00Z",
  "temperature_c": 31.2,
  "feels_like_c": 36.0,
  "humidity_percent": 75,
  "wind_speed_ms": 3.2,
  "wind_direction_deg": 190,
  "pressure_hpa": 1007,
  "weather_code": "thunderstorms",
  "source": "external_api_name"
}


Error responses:

External API timeout:

{
  "error": "UPSTREAM_TIMEOUT",
  "message": "Weather provider did not respond within 3.0 seconds"
}


Invalid location parameters:

{
  "error": "VALIDATION_ERROR",
  "message": "Invalid coordinates: lat must be between -90 and 90"
}

3.3 Normalisation-Only Endpoint (No External Fetch)

This is particularly useful later for ETL/ML.

POST /weather/normalize

Request body:

Accepts a “raw payload” that mimics a common upstream structure:

{
  "temp": 302.15,
  "temp_unit": "kelvin",
  "wind_speed": 15.0,
  "wind_speed_unit": "kmh",
  "humidity": 75,
  "pressure": 1007,
  "lat": 1.3521,
  "lon": 103.8198,
  "timestamp": "2025-12-01T12:15:00Z"
}


Response:

Same NormalizedWeather format as /weather/current, but source might be "client" or "raw_input".

Behaviour:

Converts all units to your internal standard:

Temperature → °C

Wind speed → m/s

Validates allowable ranges:

Temperature: e.g. -80 to +60°C

Humidity: 0–100

Pressure: 800–1100 hPa

Returns errors if values are obviously nonsense.

3.4 Optional: Batch Normalisation

If you want a stretch goal:

POST /weather/batch-normalize

Request:

{
  "items": [
    {
      "id": "obs1",
      "payload": { /* same as /weather/normalize */ }
    },
    {
      "id": "obs2",
      "payload": { /* ... */ }
    }
  ]
}


Response:

{
  "results": [
    {
      "id": "obs1",
      "normalized": { /* NormalizedWeather */ },
      "error": null
    },
    {
      "id": "obs2",
      "normalized": null,
      "error": "VALIDATION_ERROR: humidity must be <= 100"
    }
  ]
}

4. Internal Data Models (Pydantic v2)

You’ll likely want:

# app/models/location.py
class Location(BaseModel):
    lat: float
    lon: float
    city: str | None = None
    country_code: str | None = None

# app/models/weather.py
class NormalizedWeather(BaseModel):
    location: Location
    timestamp_utc: datetime
    temperature_c: float
    feels_like_c: float | None = None
    humidity_percent: int
    wind_speed_ms: float
    wind_direction_deg: float | None = None
    pressure_hpa: float | None = None
    weather_code: str | None = None
    source: str


For /weather/normalize input:

class RawWeatherInput(BaseModel):
    temp: float
    temp_unit: Literal["celsius", "fahrenheit", "kelvin"] = "celsius"
    wind_speed: float
    wind_speed_unit: Literal["ms", "kmh", "mph"] = "ms"
    humidity: int
    pressure: float | None = None
    lat: float
    lon: float
    timestamp: datetime

5. Services & Architecture

Suggested layout:

app/
  main.py

  api/
    health.py         # /health endpoints
    weather.py        # /weather endpoints

  core/
    config.py         # API keys, timeouts (from env)
    logging_config.py # logging setup

  models/
    location.py
    weather.py
    raw_weather.py    # if you want provider-specific models

  services/
    weather_provider.py   # external API integration
    weather_normalizer.py # unit conversions, validation logic

5.1 weather_provider.py

Responsibilities:

Build URL/query for external weather API.

Call using httpx or requests with timeout.

Parse response JSON into a provider-specific Pydantic model (optional but nice).

Map provider model → RawWeatherInput or directly → NormalizedWeather.

5.2 weather_normalizer.py

Responsibilities:

Convert units:

Kelvin → °C, °F → °C, etc.

km/h → m/s, mph → m/s.

Validate ranges.

Construct NormalizedWeather.

This separation is great for:

Testing: you can test normalisation logic without network calls.

Future: swapping to a different API provider is trivial.

6. Error Handling & Logging
Error Handling

Use HTTPException from FastAPI for:

Upstream timeout → 503 Service Unavailable.

Invalid client payload → 422 (Pydantic catches this anyway).

Wrap network calls in try/except:

Timeout

Connection errors

Non-200 status codes

Logging

Set up a logger in core/logging_config.py and call it from services:

Log outbound requests:

URL, query, timeout, maybe correlation id.

Log failures with logger.error(...) + context.

In normal flows, keep logs at INFO.

7. Testing Strategy (pytest)

You want:

7.1 Unit tests

tests/test_weather_normalizer.py

Test temperature conversions (C/F/K).

Test wind speed conversions.

Test validation of out-of-range values.

tests/test_weather_provider.py

Use responses or httpx mocking to simulate API responses.

Test success, timeout, non-200 error.

7.2 API tests

Using FastAPI’s TestClient:

/health/live → 200 + { "status": "ok" }

/weather/normalize:

Valid payload → 200 with correct units.

Invalid payload (e.g. humidity 150) → 422 or 400 with clear error.

/weather/current:

Ideally mock weather_provider so you don’t hit the real API.

Test location params validation.

7.3 Fixtures

tests/conftest.py:

app fixture → returns FastAPI app instance.

client fixture → TestClient(app).

8. Docker Requirements

Simple once you have the app:

Dockerfile (outline):

FROM python:3.11-slim

WORKDIR /app

# Install system deps if needed (curl, build-essential, etc.)
RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


.dockerignore:

__pycache__
*.pyc
.venv
.env
tests
.git


You can add tests into the image later if you want, but for now just run them locally.

9. Rough 2-Week Plan for Project A

Assuming ~12h/week:

Week 1

Day 1–2:

Create repo, set up app/ structure, main.py, health endpoints.

Configure logging & basic config.

Day 3–4:

Implement NormalizedWeather and RawWeatherInput models.

Implement weather_normalizer.py with unit conversions.

Write pytest unit tests for normaliser.

Weekend:

Implement /weather/normalize endpoint + tests.

Week 2

Day 1–2:

Implement weather_provider.py with external API integration.

Handle timeouts and errors.

Day 3–4:

Implement /weather/current endpoint, wired through provider + normaliser.

Add API tests (mock provider).

Weekend:

Write Dockerfile, .dockerignore, README.

Run container locally and hit endpoints with curl or httpie.

10. How I Can Help Next

When you’ve got a first cut:

Paste:

Project tree

main.py

weather_normalizer.py

weather_provider.py

one router (weather.py)

one or two test files

I’ll go through and:

Comment on structure, naming, typing

Suggest stronger tests

Point out any edge cases or error-handling gaps

Suggest any “big-tech polish” improvements

You can also ask for a similar spec for Project B (Text Cleaning) once you’re partway through or done with Project A.