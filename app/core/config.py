from pydantic_settings import BaseSettings
from typing import Optional
from pydantic import ConfigDict

class Settings(BaseSettings):
    nea_24hr_base_url: str = "https://api-open.data.gov.sg/v2/real-time/api/twenty-four-hr-forecast"
    nea_api_key: Optional[str] = None
    nea_timeout_seconds: float = 3.0

    model_config = ConfigDict(env_file=".env")

settings = Settings()