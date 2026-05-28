from typing import Optional
from pydantic import Field

from .common import IcarAnimalEventCoreResource, IcarResource


class IcarReproAbortionEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarReproAbortionEventResource", alias="resourceType")


class IcarReproDoNotBreedEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarReproDoNotBreedEventResource", alias="resourceType")
    doNotBreed: Optional[bool] = None
    extendedReasons: Optional[list] = None


class IcarReproEmbryoFlushingEventResource(IcarResource):
    resourceType: str = Field(default="icarReproEmbryoFlushingEventResource", alias="resourceType")
    id: Optional[str] = None
    eventDateTime: Optional[str] = None
    responsible: Optional[str] = None
    contemporaryGroup: Optional[str] = None
    remark: Optional[str] = None
    location: Optional[dict] = None
    flushingMethod: Optional[str] = None
    embryoCount: Optional[int] = None
    collectionCentre: Optional[str] = None


class IcarReproEmbryoResource(IcarResource):
    resourceType: str = Field(default="icarReproEmbryoResource", alias="resourceType")
    id: Optional[dict] = None
    collectionCentre: Optional[str] = None
    dateCollected: Optional[str] = None
    donorIdentifiers: Optional[list] = None
    donorURI: Optional[str] = None
    sireIdentifiers: Optional[list] = None
    sireOfficialName: Optional[str] = None
    sireURI: Optional[str] = None


class IcarReproHeatEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarReproHeatEventResource", alias="resourceType")
    heatDetectionMethod: Optional[str] = None
    certainty: Optional[str] = None
    commencementDateTime: Optional[str] = None
    expirationDateTime: Optional[str] = None
    visualDetection: Optional[dict] = None
    optimumInseminationWindow: Optional[list] = None
    deviceHeatProbability: Optional[float] = None
    device: Optional[dict] = None


class IcarReproMatingRecommendationResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarReproMatingRecommendationResource", alias="resourceType")
    sireRecommendations: Optional[list] = None


class IcarReproParturitionEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarReproParturitionEventResource", alias="resourceType")
    isEmbryoImplant: Optional[bool] = None
    damParity: Optional[int] = None
    liveProgeny: Optional[int] = None
    totalProgeny: Optional[int] = None
    calvingEase: Optional[str] = None
    progenyDetails: Optional[list] = None


class IcarReproPregnancyCheckEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarReproPregnancyCheckEventResource", alias="resourceType")
    method: Optional[str] = None
    result: Optional[str] = None
    foetalAge: Optional[int] = None
    foetusCount: Optional[int] = None
    foetusCountMale: Optional[int] = None
    foetusCountFemale: Optional[int] = None
    exceptions: Optional[list] = None


class IcarReproSemenStrawResource(IcarResource):
    resourceType: str = Field(default="icarReproSemenStrawResource", alias="resourceType")
    id: Optional[dict] = None
    batch: Optional[str] = None
    collectionCentre: Optional[str] = None
    dateCollected: Optional[str] = None
    sireIdentifiers: Optional[list] = None
    sireOfficialName: Optional[str] = None
    sireURI: Optional[str] = None
    preservationType: Optional[str] = None
    isSexedSemen: Optional[bool] = None
    sexedGender: Optional[str] = None
    sexedPercentage: Optional[int] = None


class IcarReproStatusObservedEventResource(IcarAnimalEventCoreResource):
    resourceType: str = Field(default="icarReproStatusObservedEventResource", alias="resourceType")
    observedStatus: Optional[str] = None


class IcarGestationResource(IcarResource):
    resourceType: str = Field(default="icarGestationResource", alias="resourceType")
    id: Optional[str] = None
    animal: Optional[dict] = None
    sireIdentifiers: Optional[list] = None
    expectedCalvingDate: Optional[str] = None
