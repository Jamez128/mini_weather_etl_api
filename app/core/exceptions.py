from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

def json_safe_errors(e: ValidationError) -> list[dict]:
    errors = e.errors()
    for err in errors:
        ctx = err.get("ctx")
        if isinstance(ctx, dict) and "error" in ctx:
            ctx["error"] = str(ctx["error"])
    return errors

async def pydantic_validation_error_handler(_: Request, exc: ValidationError):
    return JSONResponse(status_code=422, content={"detail": json_safe_errors(exc)})

async def value_error_handler(_: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
