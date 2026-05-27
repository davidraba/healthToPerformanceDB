from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query, Body

from app.services import crud_service
from app.services.resource_registry import list_registered_types, resolve_model
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination
from pydantic import ValidationError

router = APIRouter(prefix="/resources", tags=["Generic Resources"])


@router.post("")
def create_resource(payload: Dict[str, Any] = Body(...)):
    resource_type = payload.get("resourceType")
    if not resource_type:
        raise HTTPException(422, "resourceType is required")
    try:
        validate_payload(resource_type, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(resource_type, payload)
    return doc


@router.get("")
def list_resources(
    resourceType: Optional[str] = Query(None),
    locationScheme: Optional[str] = None,
    locationId: Optional[str] = None,
    animalScheme: Optional[str] = None,
    animalId: Optional[str] = None,
    fromDate: Optional[str] = None,
    toDate: Optional[str] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    limit, offset = normalize_pagination(limit, offset)
    filters = {}
    if locationScheme:
        filters["locationScheme"] = locationScheme
    if locationId:
        filters["locationId"] = locationId
    if animalScheme:
        filters["animalScheme"] = animalScheme
    if animalId:
        filters["animalId"] = animalId

    if resourceType:
        items, total = crud_service.list_all(resourceType, limit, offset, filters)
    else:
        items, total = crud_service.list_all_from_all_tables()
        items = items[offset : offset + limit]
        total = len(items)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/resource-types")
def get_resource_types():
    return {"resource_types": list_registered_types()}


@router.get("/{internal_id}")
def get_resource(internal_id: str, resourceType: str = Query(...)):
    item = crud_service.get_by_id(resourceType, internal_id)
    if not item:
        raise HTTPException(404, "Resource not found")
    return item


@router.put("/{internal_id}")
def update_resource(
    internal_id: str,
    resourceType: str = Query(...),
    payload: Dict[str, Any] = Body(...),
):
    item = crud_service.update(resourceType, internal_id, payload)
    if not item:
        raise HTTPException(404, "Resource not found")
    return item


@router.patch("/{internal_id}")
def patch_resource(
    internal_id: str,
    resourceType: str = Query(...),
    updates: Dict[str, Any] = Body(...),
):
    item = crud_service.patch(resourceType, internal_id, updates)
    if not item:
        raise HTTPException(404, "Resource not found")
    return item


@router.delete("/{internal_id}")
def delete_resource(internal_id: str, resourceType: str = Query(...)):
    deleted = crud_service.delete(resourceType, internal_id)
    if not deleted:
        raise HTTPException(404, "Resource not found")
    return {"deleted": True}
