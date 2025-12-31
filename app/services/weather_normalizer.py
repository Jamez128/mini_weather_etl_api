from app.models.weather import NormalisedWeather
from app.models.raw_weather import RawWeatherInput
from app.services.weather_helpers import convert_wind_speed, safe_feels_like_c, convert_temperature

def normalise_weather(raw: RawWeatherInput, source: str) -> NormalisedWeather:
    
    location = raw.location
    timestamp_utc = raw.timestamp
    temperature_c = raw.temp if raw.temp_unit == "Degrees Celsius" else convert_temperature(raw.temp, raw.temp_unit) 
    # RawWeatherInput defines as     temp_unit: Literal["Degrees Celsius", "Degrees Fahrenheit","Kelvin"] = "Degrees Celsius"
    if raw.humidity_unit != "Percentage":
        raise ValueError(f"Unsupported humidity unit: {raw.humidity_unit}")
    humidity_percent = raw.humidity 
    feels_like_c = safe_feels_like_c(temperature_c, humidity_percent) if humidity_percent is not None else None
    wind_speed_ms = raw.wind_speed if raw.wind_speed_unit == "ms" else convert_wind_speed(raw.wind_speed, raw.wind_speed_unit)
    wind_direction = raw.wind_dir 
    pressure_hpa = raw.pressure # not provided in NEA, raw.pressure
    weather_text = raw.forecast_description

    return NormalisedWeather(
    location = location,
    timestamp_utc = timestamp_utc,
    temperature_c = temperature_c,
    feels_like_c = feels_like_c,
    humidity_percent = humidity_percent,
    wind_speed_ms = wind_speed_ms,
    wind_direction = wind_direction,
    pressure_hpa = pressure_hpa,
    weather_text = weather_text,
    source = source
)