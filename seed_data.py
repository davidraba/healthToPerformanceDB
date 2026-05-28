from app.database import db, get_table
from app.services.crud_service import create

LOCATION = {"scheme": "es.rea", "id": "ES430000001"}
ANIMAL = {"scheme": "es.magrama.bovine", "id": "ES091234567890"}


def seed():
    create(
        "icarAnimalCoreResource",
        {
            "resourceType": "icarAnimalCoreResource",
            "identifier": ANIMAL,
            "specie": "Cattle",
            "gender": "Female",
            "birthDate": "2026-03-15T08:00:00Z",
            "status": "Active",
            "location": LOCATION,
            "primaryBreed": {"scheme": "es.rae", "id": "LIM"},
            "managementTag": "T-001",
            "productionPurpose": "Milk",
            "reproductionStatus": "Nulliparous",
        },
    )

    create(
        "icarMovementBirthEventResource",
        {
            "resourceType": "icarMovementBirthEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2026-03-15T08:00:00Z",
            "remark": "Birth of a female Limousin calf",
        },
    )

    create(
        "icarWeightEventResource",
        {
            "resourceType": "icarWeightEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2026-03-15T08:30:00Z",
            "remark": "Birth weight",
        },
    )

    create(
        "icarTreatmentEventResource",
        {
            "resourceType": "icarTreatmentEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2026-03-18T10:00:00Z",
            "remark": "Neonatal diarrhea - oral electrolytes administered",
        },
    )

    create(
        "icarTreatmentProgramEventResource",
        {
            "resourceType": "icarTreatmentProgramEventResource",
            "location": LOCATION,
            "eventDateTime": "2026-03-18T10:00:00Z",
            "remark": "Mild neonatal diarrhea treatment protocol",
        },
    )

    create(
        "icarAnimalSetResource",
        {
            "resourceType": "icarAnimalSetResource",
            "name": "Calf rearing group Q1-2026",
            "location": LOCATION,
        },
    )

    create(
        "icarGroupWeightEventResource",
        {
            "resourceType": "icarGroupWeightEventResource",
            "location": LOCATION,
            "eventDateTime": "2026-04-01T09:00:00Z",
            "remark": "Group weight check - rearing batch",
        },
    )

    create(
        "icarReproHeatEventResource",
        {
            "resourceType": "icarReproHeatEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2026-06-01T07:00:00Z",
            "heatDetectionMethod": "Visual",
            "certainty": "High",
        },
    )

    create(
        "icarReproInseminationEventResource",
        {
            "resourceType": "icarReproInseminationEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2026-06-01T14:00:00Z",
            "remark": "First insemination",
        },
    )

    create(
        "icarReproPregnancyCheckEventResource",
        {
            "resourceType": "icarReproPregnancyCheckEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2026-07-01T09:00:00Z",
            "method": "Ultrasound",
            "result": "Pregnant",
        },
    )

    create(
        "icarMilkingVisitEventResource",
        {
            "resourceType": "icarMilkingVisitEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2027-01-15T06:00:00Z",
            "remark": "Morning milking",
        },
    )

    create(
        "icarAttentionEventResource",
        {
            "resourceType": "icarAttentionEventResource",
            "animal": ANIMAL,
            "location": LOCATION,
            "eventDateTime": "2026-03-18T08:00:00Z",
            "category": "Health",
            "causes": ["Digestive"],
            "priority": "Medium",
        },
    )

    create(
        "icarFeedResource",
        {
            "resourceType": "icarFeedResource",
            "id": "FEED-CALF-001",
            "name": "Calf Starter Pellets",
            "category": "Concentrate",
            "location": LOCATION,
            "active": True,
        },
    )

    create(
        "icarRationResource",
        {
            "resourceType": "icarRationResource",
            "id": "RATION-CALF-001",
            "name": "Calf rearing ration Q1",
            "location": LOCATION,
            "active": True,
        },
    )

    create(
        "icarDeviceResource",
        {
            "resourceType": "icarDeviceResource",
            "id": "SCALE-001",
            "serial": "SN-9420-X",
            "name": "Weighing Scale Barn A",
            "isActive": True,
            "location": LOCATION,
        },
    )

    create(
        "icarMedicineResource",
        {
            "resourceType": "icarMedicineResource",
            "name": "Oral electrolyte solution",
            "approved": "Yes",
            "location": LOCATION,
        },
    )

    create(
        "icarLocationResource",
        {
            "resourceType": "icarLocationResource",
            "identifier": LOCATION,
            "name": "La Vega Experimental Farm",
            "timeZoneId": "Europe/Madrid",
        },
    )

    print("Seed data inserted successfully with all resource type examples.")


if __name__ == "__main__":
    seed()
