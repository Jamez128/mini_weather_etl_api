from pydantic import BaseModel
from typing import Literal
from datetime import datetime

class RawWeatherInput(BaseModel):
    temperature: float
    temp_unit: Literal["celsius", "fahrenheit","kelvin"] = "celsius"
    wind_speed: float
    wind_speed_unit: Literal["ms","kmh","mph"] = "ms"
    humidity: int
    pressure: float | None = None
    lat: float
    lon: float
    timestamp: datetime