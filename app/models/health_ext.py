from typing import Optional
from pydantic import Field

from .common import IcarAnimalEventCoreResource


class IcarWithdrawalEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarWithdrawalEventResource", alias="resourceType")
    endDateTime: Optional[str] = None
    productType: Optional[str] = None


class IcarAttentionEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarAttentionEventResource", alias="resourceType")
    alertEndDateTime: Optional[str] = None
    category: Optional[str] = None
    causes: Optional[list] = None
    priority: Optional[str] = None
    severity: Optional[str] = None
    deviceAttentionScore: Optional[float] = None
    device: Optional[dict] = None


class IcarDiagnosisEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarDiagnosisEventResource", alias="resourceType")
    diagnoses: Optional[list] = None


class IcarHealthStatusObservedEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarHealthStatusObservedEventResource", alias="resourceType")
    observedStatus: Optional[str] = None


class IcarRemarkEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarRemarkEventResource", alias="resourceType")
    note: Optional[str] = None



