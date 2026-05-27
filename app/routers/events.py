from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.services.resource_registry import list_registered_types
from app.utils.pagination import normalize_pagination

router = APIRouter(prefix="/events", tags=["Events"])

EVENT_TYPES = [t for t in list_registered_types() if "Event" in t]


@router.post("")
def create_event(payload: Dict[str, Any] = Body(...)):
    resource_type = payload.get("resourceType")
    if not resource_type:
        raise HTTPException(422, "resourceType is required")
    if resource_type not in EVENT_TYPES:
        raise HTTPException(422, f"Unknown event type: {resource_type}")
    try:
        validate_payload(resource_type, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(resource_type, payload)
    return doc


@router.get("")
def list_events(
    resourceType: Optional[str] = Query(None),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    limit, offset = normalize_pagination(limit, offset)
    rt = resourceType if resourceType else None
    if rt:
        items, total = crud_service.list_all(rt, limit, offset)
    else:
        items = []
        total = 0
        for et in EVENT_TYPES:
            part, _ = crud_service.list_all(et, 10000, 0)
            items.extend(part)
        total = len(items)
        items = items[offset : offset + limit]
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{internal_id}")
def get_event(internal_id: str):
    for et in EVENT_TYPES:
        item = crud_service.get_by_id(et, internal_id)
        if item:
            return item
    raise HTTPException(404, "Event not found")


@router.delete("/{internal_id}")
def delete_event(internal_id: str):
    for et in EVENT_TYPES:
        item = crud_service.get_by_id(et, internal_id)
        if item:
            crud_service.delete(et, internal_id)
            return {"deleted": True}
    raise HTTPException(404, "Event not found")


@router.get("/by-animal/{scheme}/{animal_id}")
def get_events_by_animal(scheme: str, animal_id: str):
    from app.database import get_table

    results = []
    for et in EVENT_TYPES:
        table = get_table(et)
        for doc in table.all():
            animal = doc.get("payload", {}).get("animal", {})
            if animal.get("scheme") == scheme and animal.get("id") == animal_id:
                results.append(doc)
    return {"items": results, "total": len(results)}


@router.get("/by-location/{scheme}/{location_id}")
def get_events_by_location(scheme: str, location_id: str):
    from app.database import get_table

    results = []
    for et in EVENT_TYPES:
        table = get_table(et)
        for doc in table.all():
            loc = doc.get("payload", {}).get("location", {})
            if loc.get("scheme") == scheme and loc.get("id") == location_id:
                results.append(doc)
    return {"items": results, "total": len(results)}


@router.get("/by-type/{resource_type}")
def get_events_by_type(
    resource_type: str, limit: Optional[int] = None, offset: Optional[int] = None
):
    if resource_type not in EVENT_TYPES:
        raise HTTPException(422, f"Unknown event type: {resource_type}")
    limit, offset = normalize_pagination(limit, offset)
    items, total = crud_service.list_all(resource_type, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}
