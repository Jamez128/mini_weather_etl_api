from pydantic import BaseModel
from typing import Optional

class Location(BaseModel):
    lat: float
    lon: float
    city: Optional[str]
    country_code: Optional[str]

# singapore = Location(lat=1.3521, lon=103.8198, city="Singapore", country_code="SG")
# print(singapore)