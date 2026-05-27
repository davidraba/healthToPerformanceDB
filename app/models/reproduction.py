from pydantic import Field

from .common import IcarAnimalEventCoreResource


class IcarReproInseminationEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarReproInseminationEventResource", alias="resourceType"
    )
