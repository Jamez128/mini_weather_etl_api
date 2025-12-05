🌦️ Weather Normalisation & Enrichment API

A production-style FastAPI microservice for fetching, normalising, validating, and exposing weather data.

🔧 Overview

This service provides:

Current weather data fetched from a configurable 3rd-party API

Normalised & validated weather readings using strict Pydantic v2 schemas

Conversion of temperature, wind speed, and pressure units into a consistent internal format

Error-handled, testable API endpoints suitable for downstream systems, ML pipelines, or analytics workflows

The project is intentionally engineered to reflect real-world backend/API + ML-preprocessing patterns, following clean code, modularity, and reliability standards.

🎯 Core Responsibilities

Fetch raw weather data from an external provider (with timeouts & error handling)

Normalise:

Units (°C/°F/K, m/s vs km/h vs mph)

Field names (provider-specific → internal schema)

Validate:

Temperature, humidity, pressure ranges

Required fields

Expose a clean, predictable API surface:

/weather/current

/weather/normalize

/weather/batch-normalize (optional stretch)

Provide reliability endpoints:

/health/live

/health/ready

Maintain high engineering quality:

PEP8, typing, docstrings

pytest unit/integration tests

Dockerised deployment

🧱 Architecture & Directory Layout
app/
  main.py                     # App creation, router registration

  api/
    health.py                 # Health/liveness/readiness endpoints
    weather.py                # Weather endpoints

  core/
    config.py                 # Settings (API keys, timeouts, env vars)
    logging_config.py         # Logger setup

  models/
    location.py               # Location models
    weather.py                # NormalizedWeather response model
    raw_weather.py            # Raw incoming weather formats

  services/
    weather_provider.py       # External API integration + upstream calls
    weather_normalizer.py     # Unit conversion, validation, normalization logic

tests/
  conftest.py
  test_weather_normalizer.py
  test_weather_provider.py
  test_weather_api.py

📡 API Design

Base path: /api/v1 (implicit)

1. Health Endpoints
GET /health/live

Basic process uptime check.

Response

{ "status": "ok" }

GET /health/ready

Readiness probe (can later include external API reachability).

Response

{
  "status": "ready",
  "details": {
    "external_weather_api_reachable": true
  }
}

2. Current Weather: Fetch + Normalise
GET /weather/current

Supported query params

Option A — City-based:

city: str

country_code: str = "SG"

Option B — Coordinate-based:

lat: float

lon: float

Process

Validate input

Call external provider (with timeout)

Convert raw payload → RawWeatherReading

Normalise → NormalizedWeather

Return structured JSON

Example Response

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
  "source": "external_api"
}


Error Examples

Timeout:

{
  "error": "UPSTREAM_TIMEOUT",
  "message": "Weather provider did not respond within 3.0 seconds"
}


Validation:

{
  "error": "VALIDATION_ERROR",
  "message": "Invalid coordinates: lat must be between -90 and 90"
}

3. Raw Normalisation Endpoint
POST /weather/normalize

Accepts arbitrary raw weather payloads:

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


Converts everything into internal canonical format.

Behaviour Includes

K/°F → °C

km/h → m/s

Range validation (temp, humidity, pressure)

Error responses for corrupted or nonsensical values

4. Batch Normalisation (Optional)
POST /weather/batch-normalize

Request

{
  "items": [
    { "id": "obs1", "payload": { ... } },
    { "id": "obs2", "payload": { ... } }
  ]
}


Response

{
  "results": [
    { "id": "obs1", "normalized": { ... }, "error": null },
    { "id": "obs2", "normalized": null, "error": "VALIDATION_ERROR: humidity must be <= 100" }
  ]
}

📦 Pydantic Models (v2)
Location
class Location(BaseModel):
    lat: float
    lon: float
    city: str | None = None
    country_code: str | None = None

NormalizedWeather
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

RawWeatherInput
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

🔌 Services
weather_provider.py

Build external API request

Perform HTTP GET (with timeout)

Parse JSON

Map provider payload → internal raw model

Handle:

Timeout

Connection errors

Non-200 responses

weather_normalizer.py

Convert Kelvin/Fahrenheit → Celsius

Convert km/h or mph → m/s

Validate numerical ranges

Construct a NormalizedWeather object

Separation ensures:

Easy unit testing

Easy to swap weather providers

Cleaner API-layer logic

🧪 Testing (pytest)
Unit Tests

test_weather_normalizer.py

temp conversions

wind conversions

range validations

test_weather_provider.py

mock HTTP responses

simulate timeout / invalid payload

API Tests

Using FastAPI's TestClient:

/health/live

/weather/normalize

valid input

invalid ranges

/weather/current

provider mocked

invalid params

Fixtures

tests/conftest.py should define:

app fixture

client fixture

🐳 Docker
Dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app ./app

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

.dockerignore
__pycache__
*.pyc
.venv
.env
tests
.git

📅 2-Week Build Plan (For Reference)
Week 1

Implement app structure, main file, health endpoints

Add normaliser logic + unit tests

Add /weather/normalize endpoint

Week 2

Build provider service (external API)

Add /weather/current

API tests + mocking

Dockerfile + README polish

🤝 Contributing / Review

If you're iterating on this project:

Pull requests welcome

Open issues for improvements

Code reviews encouraged

I can review:

File structure

Normalisation accuracy

Test style & mocking

Error handling design

Docker best practices