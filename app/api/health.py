from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/live")
def live() -> dict[str, str]:
    # is the process up?
    return {"status": "ok"}

@router.get("/ready")
def ready() -> dict[str, str]:
    # is the service ready to serve traffic?
    return {"status": "ready"}