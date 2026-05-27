from fastapi.testclient import TestClient

from app.main import app
from app.database import drop_all

client = TestClient(app)


def setup_function():
    drop_all()


ANIMAL = {"scheme": "es.magrama.bovine", "id": "ES091234567890"}


def test_create_birth_event():
    payload = {
        "resourceType": "icarMovementBirthEventResource",
        "animal": ANIMAL,
    }
    resp = client.post("/events", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["resourceType"] == "icarMovementBirthEventResource"


def test_list_events():
    payload = {
        "resourceType": "icarMovementBirthEventResource",
        "animal": ANIMAL,
    }
    client.post("/events", json=payload)
    resp = client.get("/events")
    assert resp.status_code == 200
    assert resp.json()["total"] == 1


def test_get_events_by_animal():
    payload = {
        "resourceType": "icarMovementBirthEventResource",
        "animal": ANIMAL,
    }
    client.post("/events", json=payload)
    resp = client.get("/events/by-animal/es.magrama.bovine/ES091234567890")
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1


def test_delete_event():
    payload = {
        "resourceType": "icarMovementBirthEventResource",
        "animal": ANIMAL,
    }
    resp = client.post("/events", json=payload)
    internal_id = resp.json()["internalId"]
    resp = client.delete(f"/events/{internal_id}")
    assert resp.status_code == 200
    resp = client.get(f"/events/{internal_id}")
    assert resp.status_code == 404
