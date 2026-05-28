from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination

router = APIRouter(prefix="/lactation", tags=["Lactation"])

LACTATION_TYPES = [
    "icarLactationResource",
    "icarLactationStatusObservedEventResource",
    "icarMilkingDryOffEventResource",
    "icarDailyMilkingAveragesResource",
    "icarMilkPredictionResource",
    "icarTestDayResource",
    "icarTestDayResultEventResource",
]


@router.post("")
def create_lactation_resource(payload: Dict[str, Any] = Body(...)):
    resource_type = payload.get("resourceType")
    if not resource_type or resource_type not in LACTATION_TYPES:
        raise HTTPException(422, f"Unknown lactation resource type: {resource_type}")
    try:
        validate_payload(resource_type, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(resource_type, payload)
    return doc


@router.get("")
def list_lactation_resources(
    resourceType: Optional[str] = Query(None),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    limit, offset = normalize_pagination(limit, offset)
    rt = resourceType if resourceType in LACTATION_TYPES else None
    if rt:
        items, total = crud_service.list_all(rt, limit, offset)
    else:
        items = []
        total = 0
        for lt in LACTATION_TYPES:
            part, _ = crud_service.list_all(lt, 10000, 0)
            items.extend(part)
        total = len(items)
        items = items[offset : offset + limit]
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{internal_id}")
def get_lactation_resource(internal_id: str, resourceType: str = Query(...)):
    if resourceType not in LACTATION_TYPES:
        raise HTTPException(422, f"Unknown lactation type: {resourceType}")
    item = crud_service.get_by_id(resourceType, internal_id)
    if not item:
        raise HTTPException(404, "Lactation resource not found")
    return item


@router.get("/by-animal/{scheme}/{animal_id}")
def get_lactation_by_animal(scheme: str, animal_id: str):
    from app.database import get_table

    results = []
    for lt in LACTATION_TYPES:
        table = get_table(lt)
        for doc in table.all():
            animal = doc.get("payload", {}).get("animal", {})
            if animal.get("scheme") == scheme and animal.get("id") == animal_id:
                results.append(doc)
    return {"items": results, "total": len(results)}
