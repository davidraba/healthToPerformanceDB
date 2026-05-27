from typing import Any, Dict, Type
from pydantic import ValidationError

from app.models import IcarResource
from app.services.resource_registry import resolve_model


def validate_payload(resource_type: str, payload: Dict[str, Any]) -> IcarResource:
    model_class: Type[IcarResource] = resolve_model(resource_type)
    try:
        return model_class(**payload)
    except ValidationError as e:
        raise e
