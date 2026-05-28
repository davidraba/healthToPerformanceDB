from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse, Response

from app.services.export_service import collect_documents, build_geojson, build_json_export

router = APIRouter(prefix="/exports", tags=["Exports"])


@router.get("/json")
def export_json(
    resourceType: Optional[str] = Query(None, description="Filter by resource type"),
    fromDate: Optional[str] = Query(None, description="Start date (ISO 8601)"),
    toDate: Optional[str] = Query(None, description="End date (ISO 8601)"),
    locationScheme: Optional[str] = None,
    locationId: Optional[str] = None,
):
    docs = collect_documents(
        resource_type=resourceType,
        from_date=fromDate,
        to_date=toDate,
        location_scheme=locationScheme,
        location_id=locationId,
    )
    data = build_json_export(docs)
    return JSONResponse(
        content=data,
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=export.json"},
    )


@router.get("/geojson")
def export_geojson(
    resourceType: Optional[str] = Query(None, description="Filter by resource type"),
    fromDate: Optional[str] = Query(None, description="Start date (ISO 8601)"),
    toDate: Optional[str] = Query(None, description="End date (ISO 8601)"),
    locationScheme: Optional[str] = None,
    locationId: Optional[str] = None,
):
    docs = collect_documents(
        resource_type=resourceType,
        from_date=fromDate,
        to_date=toDate,
        location_scheme=locationScheme,
        location_id=locationId,
    )
    geojson = build_geojson(docs)
    return JSONResponse(
        content=geojson,
        media_type="application/geo+json",
        headers={"Content-Disposition": "attachment; filename=export.geojson"},
    )
