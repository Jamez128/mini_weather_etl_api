# 🌦️ Weather Normalisation & Enrichment API

FastAPI microservice that fetches weather data from a provider (currently Singapore NEA 24-hour forecast), maps it into an internal “raw” schema, normalises units/fields into a canonical model, validates ranges with Pydantic v2, and serves it via a small API.

## What this repo demonstrates
- Clean service-layer architecture (provider → mapper → normaliser → API)
- Pydantic v2 modelling + validators
- Testing strategy: unit tests + provider mocking + API tests
- Consistent error handling via global FastAPI exception handlers

## Architecture at a glance
**Provider JSON → Provider Pydantic model → `RawWeatherInput` → `NormalisedWeather` → API response**

- *Provider model* mirrors upstream JSON (NEA schema)
- *Raw model* is the internal interchange format across providers
- *Normalised model* is the final output contract (validated + consistent)

## Project layout
### `app/`
- `app/main.py` — creates the FastAPI app, registers routers, and installs global exception handlers.
- `app/api/health.py` — `/health/live` and `/health/ready` endpoints for liveness/readiness probes.
- `app/api/weather.py` — `/weather/current` (fetch+normalise) and `/weather/normalise` (normalise request payload) endpoints.
- `app/core/config.py` — runtime settings (API URL, timeouts, optional API key) loaded via pydantic-settings.
- `app/core/exceptions.py` — global exception handlers that convert `ValidationError` and `ValueError` into JSON HTTP responses.
- `app/models/location.py` — `Location` model shared by raw/normalised models.
- `app/models/raw_weather.py` — internal raw schema (`RawWeatherInput`) and provider-specific models for NEA responses.
- `app/models/weather.py` — canonical output schema (`NormalisedWeather`) plus validators for ranges.
- `app/services/weather_provider.py` — calls the upstream API and returns `RawWeatherInput` via the provider mapper.
- `app/services/nea_mapper.py` — converts the NEA provider model into `RawWeatherInput`.
- `app/services/weather_helpers.py` — pure helper functions for unit conversions and “feels like” computation.
- `app/services/weather_normalizer.py` — normalises a `RawWeatherInput` into `NormalisedWeather`.

### `tests/`
- `tests/test_nea_mapper.py` — unit test: provider JSON → provider model → raw mapping correctness.
- `tests/test_weather_provider.py` — provider tests with HTTP mocking (success + non-200 + network error).
- `tests/test_normaliser_functions.py` — unit tests for conversion/helper functions.
- `tests/test_weather_model_validators.py` — tests for Pydantic validators/range checks on the output model.
- `tests/test_api_weather.py` — API tests using `TestClient` (mocking provider + validating error responses).

## Quickstart
### 1) Create venv + install
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```
### 2) Run tests
```bash
pytest -q
```

### 3) Run the API
```bash
uvicorn app.main:app --reload
```
Open:
- Swagger UI: http://127.0.0.1:8000/docs
- Current weather: GET /weather/current
- Normalise a payload: POST /weather/normalise

## Docker
Not included yet