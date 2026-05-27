from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Body, Query
from pydantic import ValidationError

from app.services import crud_service
from app.services.validation_service import validate_payload
from app.utils.pagination import normalize_pagination

TREATMENT_TYPE = "icarTreatmentEventResource"
TREATMENT_PROGRAM_TYPE = "icarTreatmentProgramEventResource"

router = APIRouter(prefix="/health", tags=["Health"])


@router.post("/treatments")
def create_treatment(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = TREATMENT_TYPE
    try:
        validate_payload(TREATMENT_TYPE, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(TREATMENT_TYPE, payload)
    return doc


@router.get("/treatments")
def list_treatments(limit: Optional[int] = None, offset: Optional[int] = None):
    limit, offset = normalize_pagination(limit, offset)
    items, total = crud_service.list_all(TREATMENT_TYPE, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/treatments/{internal_id}")
def get_treatment(internal_id: str):
    item = crud_service.get_by_id(TREATMENT_TYPE, internal_id)
    if not item:
        raise HTTPException(404, "Treatment not found")
    return item


@router.post("/treatment-programs")
def create_treatment_program(payload: Dict[str, Any] = Body(...)):
    payload["resourceType"] = TREATMENT_PROGRAM_TYPE
    try:
        validate_payload(TREATMENT_PROGRAM_TYPE, payload)
    except ValidationError as e:
        raise HTTPException(422, {"error": "Validation failed", "details": e.errors()})
    doc = crud_service.create(TREATMENT_PROGRAM_TYPE, payload)
    return doc


@router.get("/treatment-programs")
def list_treatment_programs(limit: Optional[int] = None, offset: Optional[int] = None):
    limit, offset = normalize_pagination(limit, offset)
    items, total = crud_service.list_all(TREATMENT_PROGRAM_TYPE, limit, offset)
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/treatment-programs/{internal_id}")
def get_treatment_program(internal_id: str):
    item = crud_service.get_by_id(TREATMENT_PROGRAM_TYPE, internal_id)
    if not item:
        raise HTTPException(404, "Treatment program not found")
    return item
