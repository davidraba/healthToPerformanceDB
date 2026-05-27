from typing import Dict, Type

from app.models import (
    IcarAnimalCoreResource,
    IcarMovementBirthEventResource,
    IcarWeightEventResource,
    IcarTreatmentEventResource,
    IcarTreatmentProgramEventResource,
    IcarGroupWeightEventResource,
    IcarMovementArrivalEventResource,
    IcarMovementDepartureEventResource,
    IcarMovementDeathEventResource,
    IcarAnimalSetJoinEventResource,
    IcarAnimalSetLeaveEventResource,
    IcarGroupTreatmentEventResource,
    IcarReproInseminationEventResource,
    IcarMilkingVisitEventResource,
    IcarAnimalSetResource,
    GenericIcarResource,
    IcarResource,
)

RESOURCE_MODEL_REGISTRY: Dict[str, Type[IcarResource]] = {
    "icarAnimalCoreResource": IcarAnimalCoreResource,
    "icarMovementBirthEventResource": IcarMovementBirthEventResource,
    "icarWeightEventResource": IcarWeightEventResource,
    "icarTreatmentEventResource": IcarTreatmentEventResource,
    "icarTreatmentProgramEventResource": IcarTreatmentProgramEventResource,
    "icarGroupWeightEventResource": IcarGroupWeightEventResource,
    "icarMovementArrivalEventResource": IcarMovementArrivalEventResource,
    "icarMovementDepartureEventResource": IcarMovementDepartureEventResource,
    "icarMovementDeathEventResource": IcarMovementDeathEventResource,
    "icarAnimalSetJoinEventResource": IcarAnimalSetJoinEventResource,
    "icarAnimalSetLeaveEventResource": IcarAnimalSetLeaveEventResource,
    "icarGroupTreatmentEventResource": IcarGroupTreatmentEventResource,
    "icarReproInseminationEventResource": IcarReproInseminationEventResource,
    "icarMilkingVisitEventResource": IcarMilkingVisitEventResource,
    "icarAnimalSetResource": IcarAnimalSetResource,
}


def resolve_model(resource_type: str) -> Type[IcarResource]:
    return RESOURCE_MODEL_REGISTRY.get(resource_type, GenericIcarResource)


def is_registered(resource_type: str) -> bool:
    return resource_type in RESOURCE_MODEL_REGISTRY


def list_registered_types() -> list[str]:
    return list(RESOURCE_MODEL_REGISTRY.keys())
