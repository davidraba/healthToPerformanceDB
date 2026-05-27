from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import APP_TITLE, APP_VERSION, APP_DESCRIPTION

from app.routers import (
    animals,
    events,
    generic_resources,
    groups,
    devices,
    medicines,
    locations,
    health,
    weights,
)

app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)},
    )


@app.get("/healthcheck", tags=["System"])
def healthcheck():
    return {"status": "ok", "version": APP_VERSION}


app.include_router(generic_resources.router)
app.include_router(animals.router)
app.include_router(events.router)
app.include_router(groups.router)
app.include_router(devices.router)
app.include_router(medicines.router)
app.include_router(locations.router)
app.include_router(health.router)
app.include_router(weights.router)
