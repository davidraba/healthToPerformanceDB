from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query

from app.services import crud_service
from app.utils.pagination import normalize_pagination

MEDICINE_TYPE = "icarMedicineResource"

router = APIRouter(prefix="/medicines", tags=["Medicines"])


@router.post("")
def create_medicine(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = MEDICINE_TYPE
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
