import json
from app.models.raw_weather import Nea24hForecastResponse

with open('provider_sample_response.json') as f:
    raw = json.load(f)

nea = Nea24hForecastResponse.model_validate(raw)
print(nea)