from pydantic import BaseModel
from location import Location
from datetime import datetime
from typing import Optional

class NormalisedWeather(BaseModel):
    location: Location
    timestamp_utc: datetime
    temperature_c: float
    feels_like_c: Optional[float] = None
    humidity_percent: int
    wind_speed_ms: int
    wind_direction: Optional[str] = None
    pressure_hpa: Optional[float] = None
    weather_code: Optional[str] = None
    weather_text: Optional[str] = None
    source: str
