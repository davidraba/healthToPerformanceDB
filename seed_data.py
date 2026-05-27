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

    print("Seed data inserted successfully.")


if __name__ == "__main__":
    seed()
