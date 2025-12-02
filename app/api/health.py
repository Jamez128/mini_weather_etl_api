from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter()

@router.get("/health/live")
def live() -> dict:
    return {"status": "ok"}

@router.get("/health/ready")
def ready() -> dict:
    # for now: always ready
    return {
        "status": "ready",
        "details": {
            "external_weather_api_reachable": True, # make real later
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    }
# test using `uvicorn app.main:app --reload` in cli