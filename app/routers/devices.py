from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.resource_registry import resolve_model
from app.utils.pagination import normalize_pagination

DEVICE_TYPE = "icarDeviceResource"

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.post("")
def create_device(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = DEVICE_TYPE
    doc = crud_service.create(DEVICE_TYPE, payload)
    return doc


@router.get("")
def list_devices(limit: Optional[int] = None, offset: Optional[int] = None):
    limit, offset = normalize_pagination(limit, offset)
    items, total = crud_service.list_all(DEVICE_TYPE, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/{internal_id}")
def get_device(internal_id: str):
    item = crud_service.get_by_id(DEVICE_TYPE, internal_id)
    if not item:
        raise HTTPException(404, "Device not found")
    return item
