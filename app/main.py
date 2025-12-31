from fastapi import FastAPI
from pydantic import ValidationError
from app.core.exceptions import pydantic_validation_error_handler, value_error_handler
from app.api.health import router as health_router
from app.api.weather import router as weather_router

app = FastAPI(title="Weather Normalisation API", version="0.1.0")

app.include_router(health_router)
app.include_router(weather_router)

app.add_exception_handler(ValidationError, pydantic_validation_error_handler)
app.add_exception_handler(ValueError, value_error_handler)