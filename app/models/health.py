from typing import Optional
from pydantic import Field

from .common import IcarAnimalEventCoreResource, IcarEventCoreResource


class IcarTreatmentEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarTreatmentEventResource", alias="resourceType"
    )


class IcarTreatmentProgramEventResource(IcarEventCoreResource):
    resourceType: str = Field(
        default="icarTreatmentProgramEventResource", alias="resourceType"
    )


class IcarGroupTreatmentEventResource(IcarEventCoreResource):
    resourceType: str = Field(
        default="icarGroupTreatmentEventResource", alias="resourceType"
    )
