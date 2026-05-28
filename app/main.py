import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

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
    feeds,
    reproduction_ext,
    lactation_router,
    health_ext_router,
    group_movements,
    exports,
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


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(os.path.join(STATIC_DIR, "favicon.ico"), media_type="image/x-icon")


@app.get("/", include_in_schema=False)
async def landing():
    return FileResponse(os.path.join(STATIC_DIR, "landing.html"), media_type="text/html")


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
app.include_router(feeds.router)
app.include_router(reproduction_ext.router)
app.include_router(lactation_router.router)
app.include_router(health_ext_router.router)
app.include_router(group_movements.router)
app.include_router(exports.router)
