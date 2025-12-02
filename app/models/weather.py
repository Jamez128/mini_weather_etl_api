from pydantic import BaseModel
from location import Location
from datetime import datetime

class NormalisedWeather(BaseModel):
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
