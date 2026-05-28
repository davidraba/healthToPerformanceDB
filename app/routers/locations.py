from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination

LOCATION_TYPE = "icarLocationResource"

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.post("")
def create_location(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = LOCATION_TYPE
    try:
        validate_payload(LOCATION_TYPE, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
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


@router.delete("/{internal_id}")
def delete_location(internal_id: str):
    deleted = crud_service.delete(LOCATION_TYPE, internal_id)
    if not deleted:
        raise HTTPException(404, "Location not found")
    return {"deleted": True}
