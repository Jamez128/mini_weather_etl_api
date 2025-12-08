import json
from pathlib import Path

from app.models.raw_weather import Nea24hForecastResponse
from app.services.nea_mapper import map_nea_to_raw

def test_map_nea_to_raw_uses_ranges_correctly():
    # Arrange: load the saved NEA sample response
    sample_path = Path("provider_sample_response.json")
    raw_json = json.loads(sample_path.read_text())

    # Act: validate into NEA model, then map to RawWeatherInput
    nea_model = Nea24hForecastResponse.model_validate(raw_json)
    raw = map_nea_to_raw(nea_model)

    # Grab the "general" section to compare against
    records = nea_model.data.records[0]
    general = records.general

    # Assert: temperature is between low/high
    assert general.temperature.low <= raw.temp <= general.temperature.high
    
    # humidity is between low/high
    assert general.relativeHumidity.low <= raw.humidity <= general.relativeHumidity.high

    # wind speed is between low/high
    assert general.wind.speed.low <= raw.wind_speed <= general.wind.speed.high

    # timestamp matches updatedTimestamp
    assert records.updatedTimestamp == raw.timestamp

    # forecast test matches
    assert general.forecast.text == raw.forecast_description

    # wind direction matches
    assert general.wind.direction == raw.wind_dir

    


