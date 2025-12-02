from pydantic import BaseModel

class Location(BaseModel):
    lat: float
    lon: float
    city: str | None = None
    country_code: str | None = None

# singapore = Location(lat=1.3521, lon=103.8198, city="Singapore", country_code="SG")
# print(singapore)