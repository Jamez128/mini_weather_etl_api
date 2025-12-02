from fastapi import FastAPI

from app.api import health #weather

def create_app() -> FastAPI:
    app = FastAPI(title="Weather Normalisation API")

    app.include_router(health.router, prefix="", tags=["health"])
    # weather router will be wired later:
    # app.include_router(weather.router, prefix="/weather", tages=["weather"])

    return app

app = create_app()
