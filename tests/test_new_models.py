from fastapi.testclient import TestClient

from app.main import app
from app.database import drop_all

client = TestClient(app)


def setup_function():
    drop_all()


def test_resource_types_count():
    resp = client.get("/resources/resource-types")
    assert resp.status_code == 200
    types = resp.json()["resource_types"]
    assert len(types) >= 60


def test_create_heat_event_via_resources():
    resp = client.post("/resources", json={
        "resourceType": "icarReproHeatEventResource",
        "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "eventDateTime": "2026-04-01T09:00:00Z",
        "heatDetectionMethod": "Visual"
    })
    assert resp.status_code == 200


def test_create_pregnancy_check_via_reproduction_router():
    resp = client.post("/reproduction", json={
        "resourceType": "icarReproPregnancyCheckEventResource",
        "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "eventDateTime": "2026-05-01T09:00:00Z",
        "result": "Pregnant"
    })
    assert resp.status_code == 200


def test_create_feed_via_feeding_router():
    resp = client.post("/feeding", json={
        "resourceType": "icarFeedResource",
        "id": "FEED-001",
        "name": "Calf Starter",
        "active": True
    })
    assert resp.status_code == 200


def test_create_device_with_validation():
    resp = client.post("/devices", json={
        "id": "DEV-001",
        "serial": "RF-9420",
        "name": "Ear tag RFID"
    })
    assert resp.status_code == 200


def test_create_location_with_validation():
    resp = client.post("/locations", json={
        "identifier": {"scheme": "es.rea", "id": "ES430000001"},
        "name": "La Vega"
    })
    assert resp.status_code == 200


def test_get_device_not_found():
    resp = client.get("/devices/nonexistent-id")
    assert resp.status_code == 404


def test_create_feed_transaction():
    resp = client.post("/resources", json={
        "resourceType": "icarFeedTransactionResource",
        "quantity": 500.0,
        "unit": "kg",
        "product": {"scheme": "org.feed", "id": "FEED-001"}
    })
    assert resp.status_code == 200
