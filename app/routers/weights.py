from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination

WEIGHT_TYPE = "icarWeightEventResource"
GROUP_WEIGHT_TYPE = "icarGroupWeightEventResource"

router = APIRouter(prefix="/weights", tags=["Weights"])


@router.post("")
def create_weight(payload: Dict[str, Any] = Body(...)):
    resource_type = payload.get("resourceType", WEIGHT_TYPE)
    try:
        validate_payload(resource_type, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(resource_type, payload)
    return doc


@router.get("")
def list_weights(
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    locationScheme: Optional[str] = None,
    locationId: Optional[str] = None,
):
    limit, offset = normalize_pagination(limit, offset)
    filters = {}
    if locationScheme:
        filters["locationScheme"] = locationScheme
    if locationId:
        filters["locationId"] = locationId
    items, total = crud_service.list_all(WEIGHT_TYPE, limit, offset, filters)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{internal_id}")
def get_weight(internal_id: str):
    item = crud_service.get_by_id(WEIGHT_TYPE, internal_id)
    if not item:
        item = crud_service.get_by_id(GROUP_WEIGHT_TYPE, internal_id)
    if not item:
        raise HTTPException(404, "Weight not found")
    return item


@router.get("/by-animal/{scheme}/{animal_id}")
def get_weights_by_animal(scheme: str, animal_id: str):
    from app.database import get_table

    results = []
    for wt in [WEIGHT_TYPE]:
        table = get_table(wt)
        for doc in table.all():
            animal = doc.get("payload", {}).get("animal", {})
            if animal.get("scheme") == scheme and animal.get("id") == animal_id:
                results.append(doc)
    return {"items": results, "total": len(results)}


@router.get("/by-location/{scheme}/{location_id}")
def get_weights_by_location(scheme: str, location_id: str):
    from app.database import get_table

    results = []
    for wt in [WEIGHT_TYPE, GROUP_WEIGHT_TYPE]:
        table = get_table(wt)
        for doc in table.all():
            loc = doc.get("payload", {}).get("location", {})
            if loc.get("scheme") == scheme and loc.get("id") == location_id:
                results.append(doc)
    return {"items": results, "total": len(results)}
