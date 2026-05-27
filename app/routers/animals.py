from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.services.resource_registry import resolve_model
from app.utils.pagination import normalize_pagination

ANIMAL_TYPE = "icarAnimalCoreResource"

router = APIRouter(prefix="/animals", tags=["Animals"])


@router.post("")
def create_animal(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = ANIMAL_TYPE
    scheme = payload.get("identifier", {}).get("scheme")
    animal_id = payload.get("identifier", {}).get("id")
    if not scheme or not animal_id:
        raise HTTPException(422, "identifier.scheme and identifier.id are required")
    if crud_service.exists_by_identifier(ANIMAL_TYPE, scheme, animal_id):
        raise HTTPException(409, f"Animal {scheme}/{animal_id} already exists")
    try:
        validate_payload(ANIMAL_TYPE, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(ANIMAL_TYPE, payload)
    return doc


@router.get("")
def list_animals(
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
    items, total = crud_service.list_all(ANIMAL_TYPE, limit, offset, filters)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{scheme}/{animal_id}")
def get_animal(scheme: str, animal_id: str):
    item = crud_service.get_by_identifier(ANIMAL_TYPE, scheme, animal_id)
    if not item:
        raise HTTPException(404, "Animal not found")
    return item


@router.put("/{scheme}/{animal_id}")
def update_animal(scheme: str, animal_id: str, payload: Dict[str, Any] = Body(...)):
    existing = crud_service.get_by_identifier(ANIMAL_TYPE, scheme, animal_id)
    if not existing:
        raise HTTPException(404, "Animal not found")
    payload["resourceType"] = ANIMAL_TYPE
    internal_id = existing["internalId"]
    doc = crud_service.update(ANIMAL_TYPE, internal_id, payload)
    return doc


@router.patch("/{scheme}/{animal_id}")
def patch_animal(scheme: str, animal_id: str, updates: Dict[str, Any] = Body(...)):
    existing = crud_service.get_by_identifier(ANIMAL_TYPE, scheme, animal_id)
    if not existing:
        raise HTTPException(404, "Animal not found")
    internal_id = existing["internalId"]
    doc = crud_service.patch(ANIMAL_TYPE, internal_id, updates)
    return doc


@router.delete("/{scheme}/{animal_id}")
def delete_animal(scheme: str, animal_id: str):
    existing = crud_service.get_by_identifier(ANIMAL_TYPE, scheme, animal_id)
    if not existing:
        raise HTTPException(404, "Animal not found")
    internal_id = existing["internalId"]
    crud_service.delete(ANIMAL_TYPE, internal_id)
    return {"deleted": True}


@router.get("/{scheme}/{animal_id}/events")
def get_animal_events(scheme: str, animal_id: str):
    from app.database import all_tables, get_table

    results = []
    for table_name in all_tables():
        if table_name == ANIMAL_TYPE:
            continue
        table = get_table(table_name)
        for doc in table.all():
            payload = doc.get("payload", {})
            animal = payload.get("animal", {})
            if animal.get("scheme") == scheme and animal.get("id") == animal_id:
                results.append(doc)
    return {"items": results, "total": len(results)}
