from app.services.resource_registry import resolve_model
from typing import Any, Dict


def validate_json_structure(payload: Dict[str, Any]) -> list[str]:
    errors = []
    resource_type = payload.get("resourceType")
    if not resource_type:
        errors.append("resourceType is required")
        return errors
    model_class = resolve_model(resource_type)
    if model_class.__name__ == "GenericIcarResource":
        return []
    fields = model_class.model_fields
    for field_name, field_info in fields.items():
        if field_info.is_required():
            json_key = field_info.alias or field_name
            if json_key not in payload:
                errors.append(f"Missing required field: {json_key}")
    return errors
