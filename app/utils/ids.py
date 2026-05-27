import uuid


def generate_internal_id() -> str:
    return str(uuid.uuid4())
