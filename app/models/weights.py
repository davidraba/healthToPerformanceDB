from typing import Optional
from pydantic import Field

from .common import IcarAnimalEventCoreResource, IcarEventCoreResource


class IcarWeightEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarWeightEventResource", alias="resourceType")


class IcarGroupWeightEventResource(IcarEventCoreResource):
    resourceType: str = Field(
        default="icarGroupWeightEventResource", alias="resourceType"
    )
