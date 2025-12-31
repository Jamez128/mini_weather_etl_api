from pydantic import BaseModel, field_validator
from app.models.location import Location
from datetime import datetime
from typing import Optional

class NormalisedWeather(BaseModel):
    location: Location
    timestamp_utc: datetime
    temperature_c: float
    feels_like_c: Optional[float] = None
    humidity_percent: int
    wind_speed_ms: float
    wind_direction: Optional[str] = None
    pressure_hpa: Optional[float] = None
    weather_code: Optional[str] = None
    weather_text: Optional[str] = None
    source: str

    # ---------- validators ----------

    @field_validator("temperature_c")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        if not -80 <= v <= 60:
            raise ValueError("temperature_c must be between -80 and 60 deg c")
        return v

    @field_validator("humidity_percent")
    @classmethod
    def validate_humidity(cls, v: int) -> int:
        if not 0 <= v <= 100:
            raise ValueError("humidity_percent must be between 0 and 100")
        return v

    @field_validator("wind_speed_ms")
    @classmethod
    def validate_wind_speed(cls, v: float) -> float:
        if v < 0:
            raise ValueError("wind_speed_ms must be >= 0")
        return v

    @field_validator("pressure_hpa")
    @classmethod
    def validate_pressure(cls, v: Optional[float]) -> Optional[float]:
        if v is None:
            return v
        if not 800 <= v <= 1100:
            raise ValueError("pressure_hpa must be between 800 and 1100")
        return v
