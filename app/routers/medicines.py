from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination

MEDICINE_TYPE = "icarMedicineResource"

router = APIRouter(prefix="/medicines", tags=["Medicines"])


@router.post("")
def create_medicine(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = MEDICINE_TYPE
    try:
        validate_payload(MEDICINE_TYPE, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(MEDICINE_TYPE, payload)
    return doc


@router.get("")
def list_medicines(limit: Optional[int] = None, offset: Optional[int] = None):
    limit, offset = normalize_pagination(limit, offset)
    items, total = crud_service.list_all(MEDICINE_TYPE, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{internal_id}")
def get_medicine(internal_id: str):
    item = crud_service.get_by_id(MEDICINE_TYPE, internal_id)
    if not item:
        raise HTTPException(404, "Medicine not found")
    return item


@router.delete("/{internal_id}")
def delete_medicine(internal_id: str):
    deleted = crud_service.delete(MEDICINE_TYPE, internal_id)
    if not deleted:
        raise HTTPException(404, "Medicine not found")
    return {"deleted": True}
