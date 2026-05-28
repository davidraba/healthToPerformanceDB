from typing import Optional
from pydantic import Field

from .common import IcarAnimalEventCoreResource, IcarResource


class IcarLactationResource(IcarResource):
    resourceType: str = Field(default="icarLactationResource", alias="resourceType")
    id: Optional[str] = None
    animal: Optional[dict] = None
    beginDate: Optional[str] = None
    endDate: Optional[str] = None
    parity: Optional[float] = None
    lactationLength: Optional[float] = None
    milkAmount: Optional[dict] = None
    fatAmount: Optional[dict] = None
    proteinAmount: Optional[dict] = None
    lactosisAmount: Optional[dict] = None
    lastTestDay: Optional[str] = None
    lactationType: Optional[str] = None
    milkRecordingMethod: Optional[dict] = None


class IcarLactationStatusObservedEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarLactationStatusObservedEventResource", alias="resourceType")
    observedStatus: Optional[str] = None


class IcarMilkingDryOffEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarMilkingDryOffEventResource", alias="resourceType")


class IcarDailyMilkingAveragesResource(IcarResource):
    resourceType: str = Field(default="icarDailyMilkingAveragesResource", alias="resourceType")
    id: Optional[str] = None
    animal: Optional[dict] = None
    averageDate: Optional[str] = None
    milkYieldAvg24h: Optional[dict] = None
    milkYieldAvg7days: Optional[dict] = None


class IcarMilkPredictionResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarMilkPredictionResource", alias="resourceType")
    averagePredictedProduction: Optional[dict] = None
    daysInMilkAtLactationPeak: Optional[int] = None
    lactationPeakProduction: Optional[dict] = None
    predictedProductionNextMR: Optional[dict] = None


class IcarTestDayResource(IcarResource):
    resourceType: str = Field(default="icarTestDayResource", alias="resourceType")
    id: Optional[str] = None
    beginDate: Optional[str] = None
    endDate: Optional[str] = None


class IcarTestDayResultEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarTestDayResultEventResource", alias="resourceType")
    milkWeight24Hours: Optional[dict] = None
    testDayCode: Optional[str] = None
    milkCharacteristics: Optional[list] = None
    predictedProductionOnTestDay: Optional[dict] = None
