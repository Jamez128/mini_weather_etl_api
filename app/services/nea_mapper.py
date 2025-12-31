from app.models.raw_weather import (
    RawWeatherInput,
    Nea24hForecastResponse,
    Location
)

def map_nea_to_raw(nea: Nea24hForecastResponse) -> RawWeatherInput:
    records = nea.data.records[0] # beause records is a list
    general = records.general
    avg_temp = (general.temperature.low + general.temperature.high) /2
    temp_unit = general.temperature.unit
    avg_humidity = (general.relativeHumidity.low + general.relativeHumidity.high) /2
    humidity_unit = general.relativeHumidity.unit
    avg_wind = (general.wind.speed.low + general.wind.speed.high) /2
    wind_dir = general.wind.direction
    wind_unit = "kmh"
    forecast_description = general.forecast.text
    location = "Singapore"

    # Timestamp use updatedTimestamp
    timestamp = records.updatedTimestamp

    return RawWeatherInput(
        temp=avg_temp,
        temp_unit=temp_unit,
        wind_speed=avg_wind,
        wind_speed_unit=wind_unit,
        wind_dir=wind_dir,
        humidity=int(avg_humidity),
        humidity_unit=humidity_unit,
        pressure=None,
        timestamp=timestamp,
        forecast_description=forecast_description,
        location=Location(
            lat=1.3521,
            lon=103.8198,
            city="Singapore",
            country_code="SG",
        )
    )