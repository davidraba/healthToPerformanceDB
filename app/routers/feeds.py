from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination

router = APIRouter(prefix="/feeding", tags=["Feeding"])

FEED_TYPES = [
    "icarFeedResource",
    "icarFeedStorageResource",
    "icarFeedTransactionResource",
    "icarFeedIntakeEventResource",
    "icarFeedRecommendationResource",
    "icarFeedReportResource",
    "icarRationResource",
    "icarGroupFeedingEventResource",
]


@router.post("")
def create_feed_resource(payload: Dict[str, Any] = Body(...)):
    resource_type = payload.get("resourceType")
    if not resource_type or resource_type not in FEED_TYPES:
        raise HTTPException(422, f"Unknown feed resource type: {resource_type}")
    try:
        validate_payload(resource_type, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(resource_type, payload)
    return doc


@router.get("")
def list_feed_resources(
    resourceType: Optional[str] = Query(None),
    limit: Optional[int] = None,
    offset: Optional[int] = None,
):
    limit, offset = normalize_pagination(limit, offset)
    rt = resourceType if resourceType in FEED_TYPES else None
    if rt:
        items, total = crud_service.list_all(rt, limit, offset)
    else:
        items = []
        total = 0
        for ft in FEED_TYPES:
            part, _ = crud_service.list_all(ft, 10000, 0)
            items.extend(part)
        total = len(items)
        items = items[offset : offset + limit]
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{internal_id}")
def get_feed_resource(internal_id: str, resourceType: str = Query(...)):
    if resourceType not in FEED_TYPES:
        raise HTTPException(422, f"Unknown feed type: {resourceType}")
    item = crud_service.get_by_id(resourceType, internal_id)
    if not item:
        raise HTTPException(404, "Feed resource not found")
    return item


@router.delete("/{internal_id}")
def delete_feed_resource(internal_id: str, resourceType: str = Query(...)):
    if resourceType not in FEED_TYPES:
        raise HTTPException(422, f"Unknown feed type: {resourceType}")
    deleted = crud_service.delete(resourceType, internal_id)
    if not deleted:
        raise HTTPException(404, "Feed resource not found")
    return {"deleted": True}
