from pydantic import BaseModel
from typing import Literal, Optional
from datetime import date, datetime

# ---- Canonical internal "raw" model ----

class RawWeatherInput(BaseModel):
    temp: float
    temp_unit: Literal["Degrees Celsius", "Degrees Fahrenheit","Kelvin"] = "Degrees Celsius"
    wind_speed: float
    wind_speed_unit: Literal["ms","kmh","mph"] = "ms"
    wind_dir: str
    humidity: int
    humidity_unit: str
    pressure: Optional[float] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    timestamp: datetime
    forecast_description: Optional[str] = None
    location: Optional[str] = None

# ---- NEA provider models (mirror JSON structure) ----

class NeaTemperatureRange(BaseModel):
    low: float     # temp_low = response["data"]["records"]["general"]["temperature"]["low"] # i.e., "low": 24,
    high: float     # temp_high = response["data"]["records"]["general"]["temperature"]["high"] # i.e., "high": 33,
    unit: str     # temp_unit = response["data"]["records"]["general"]["temperature"]["unit"] # i.e., "unit": "Degrees Celsius"

class NeaHumidityRange(BaseModel):
    low: int     # humid_low = response["data"]["records"]["general"]["relativeHumidity"]["low"] # i.e., "low": 60,
    high: int     # humid_high = response["data"]["records"]["general"]["relativeHumidity"]["high"] # i.e., "high": 95,
    unit: str     # humid_unit = response["data"]["records"]["general"]["relativeHumidity"]["unit"] # i.e., "unit": "Percentage"

class NeaWindSpeed(BaseModel):
    low: int     # wind_low = response["data"]["records"]["general"]["wind"]["speed"]["low"] # i.e., "low": 15,
    high: int     # wind_high = response["data"]["records"]["general"]["wind"]["speed"]["high"] # i.e., "high": 25

class NeaWindDirection(BaseModel):
    direction: str

class NeaWind(BaseModel):
    speed: NeaWindSpeed
    direction: str
    # direction: NeaWindDirection

class NeaForecastDescription(BaseModel):
    code: str     # forecast_code = response["data"]["records"]["general"]["forecast"]["code"] # i.e., "code": "TL",
    text: str     # forecast_text = response["data"]["records"]["general"]["forecast"]["text"] # i.e., "text": "Thundery Showers"

class NeaValidPeriod(BaseModel):
    text: str     # valid_range = response["data"]["records"]["general"]["validPeriod"]["text"] # i.e., "text": "6 PM 5 Dec to 6 PM 6 Dec"

class NeaGeneralForecast(BaseModel):
    temperature: NeaTemperatureRange
    relativeHumidity: NeaHumidityRange
    forecast: NeaForecastDescription
    validPeriod: NeaValidPeriod
    wind: NeaWind

class NeaRecords(BaseModel):
    date: date
    updatedTimestamp: datetime
    general: NeaGeneralForecast

class NeaData(BaseModel):
    records: list[NeaRecords]

class Nea24hForecastResponse(BaseModel):
    data: NeaData
