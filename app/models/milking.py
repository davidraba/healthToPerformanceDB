from pydantic import Field

from .common import IcarAnimalEventCoreResource


class IcarMilkingVisitEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(
        default="icarMilkingVisitEventResource", alias="resourceType"
    )
