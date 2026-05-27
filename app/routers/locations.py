from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query

from app.services import crud_service
from app.utils.pagination import normalize_pagination

LOCATION_TYPE = "icarLocationResource"

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("")
def create_location(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = LOCATION_TYPE
    doc = crud_service.create(LOCATION_TYPE, payload)
    return doc


@router.get("")
def list_locations(limit: Optional[int] = None, offset: Optional[int] = None):
    limit, offset = normalize_pagination(limit, offset)
    items, total = crud_service.list_all(LOCATION_TYPE, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{internal_id}")
def get_location(internal_id: str):
    item = crud_service.get_by_id(LOCATION_TYPE, internal_id)
    if not item:
        raise HTTPException(404, "Location not found")
    return item
