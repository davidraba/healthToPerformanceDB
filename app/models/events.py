from typing import Optional
from pydantic import Field

from .common import IcarAnimalEventCoreResource


class IcarMovementBirthEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarMovementBirthEventResource", alias="resourceType"
    )


class IcarMovementArrivalEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarMovementArrivalEventResource", alias="resourceType"
    )


class IcarMovementDepartureEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarMovementDepartureEventResource", alias="resourceType"
    )


class IcarMovementDeathEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarMovementDeathEventResource", alias="resourceType"
    )


class IcarAnimalSetJoinEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarAnimalSetJoinEventResource", alias="resourceType"
    )


class IcarAnimalSetLeaveEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarAnimalSetLeaveEventResource", alias="resourceType"
    )
