from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination

router = APIRouter(prefix="/group-movements", tags=["Group Movements"])

GROUP_MOVEMENT_TYPES = [
    "icarGroupMovementBirthEventResource",
    "icarGroupMovementArrivalEventResource",
    "icarGroupMovementDepartureEventResource",
    "icarGroupMovementDeathEventResource",
    "icarPositionObservationEventResource",
    "icarGroupPositionObservationEventResource",
]


@router.post("")
def create_group_movement(payload: Dict[str, Any] = Body(...)):
    resource_type = payload.get("resourceType")
    if not resource_type or resource_type not in GROUP_MOVEMENT_TYPES:
        raise HTTPException(422, f"Unknown group movement type: {resource_type}")
    try:
        validate_payload(resource_type, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(resource_type, payload)
    return doc


@router.get("")
def list_group_movements(
    resourceType: Optional[str] = Query(None),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    limit, offset = normalize_pagination(limit, offset)
    rt = resourceType if resourceType in GROUP_MOVEMENT_TYPES else None
    if rt:
        items, total = crud_service.list_all(rt, limit, offset)
    else:
        items = []
        total = 0
        for gt in GROUP_MOVEMENT_TYPES:
            part, _ = crud_service.list_all(gt, 10000, 0)
            items.extend(part)
        total = len(items)
        items = items[offset : offset + limit]
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/by-location/{scheme}/{location_id}")
def get_group_movements_by_location(scheme: str, location_id: str):
    from app.database import get_table

    results = []
    for gt in GROUP_MOVEMENT_TYPES:
        table = get_table(gt)
        for doc in table.all():
            loc = doc.get("payload", {}).get("location", {})
            if loc.get("scheme") == scheme and loc.get("id") == location_id:
                results.append(doc)
    return {"items": results, "total": len(results)}


@router.get("/{internal_id}")
def get_group_movement(internal_id: str, resourceType: str = Query(...)):
    if resourceType not in GROUP_MOVEMENT_TYPES:
        raise HTTPException(422, f"Unknown group movement type: {resourceType}")
    item = crud_service.get_by_id(resourceType, internal_id)
    if not item:
        raise HTTPException(404, "Group movement not found")
    return item


@router.delete("/{internal_id}")
def delete_group_movement(internal_id: str, resourceType: str = Query(...)):
    if resourceType not in GROUP_MOVEMENT_TYPES:
        raise HTTPException(422, f"Unknown group movement type: {resourceType}")
    deleted = crud_service.delete(resourceType, internal_id)
    if not deleted:
        raise HTTPException(404, "Group movement not found")
    return {"deleted": True}
