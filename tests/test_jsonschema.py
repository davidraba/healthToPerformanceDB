from fastapi.testclient import TestClient

from app.main import app
from app.database import drop_all

client = TestClient(app)


def setup_function():
    drop_all()


def test_get_schema_for_animal():
    resp = client.get("/resources/schemas/icarAnimalCoreResource")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["title"] == "IcarAnimalCoreResource"
    assert "properties" in schema
    assert "identifier" in schema["properties"]
    assert "specie" in schema["properties"]


def test_get_schema_for_new_type():
    resp = client.get("/resources/schemas/icarReproHeatEventResource")
    assert resp.status_code == 200
    props = resp.json()["properties"]
    assert "heatDetectionMethod" in props
    assert "animal" in props


def test_get_schema_for_feed_type():
    resp = client.get("/resources/schemas/icarFeedResource")
    assert resp.status_code == 200
    props = resp.json()["properties"]
    assert "name" in props
    assert "category" in props


def test_get_schema_unknown_type():
    resp = client.get("/resources/schemas/icarNonExistentResource")
    assert resp.status_code == 404


def test_validation_rejects_bad_type():
    resp = client.post("/resources", json={
        "resourceType": "icarAnimalCoreResource",
        "identifier": "should_be_an_object_not_a_string",
    })
    assert resp.status_code == 422
    error_data = resp.json()
    detail = error_data.get("detail") or error_data.get("details", [])
    assert len(detail) > 0


def test_validation_rejects_unknown_type():
    resp = client.post("/resources", json={
        "resourceType": "icarTotallyUnknownResource",
        "specie": "Cattle",
    })
    assert resp.status_code == 422


def test_both_validations_pass():
    resp = client.post("/resources", json={
        "resourceType": "icarReproPregnancyCheckEventResource",
        "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "eventDateTime": "2026-05-01T09:00:00Z",
        "method": "Ultrasound",
        "result": "Pregnant",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["resourceType"] == "icarReproPregnancyCheckEventResource"


def test_device_validation_with_schema():
    resp = client.get("/resources/schemas/icarDeviceResource")
    assert resp.status_code == 200
    props = resp.json()["properties"]
    assert "serial" in props
    assert "isActive" in props


def test_json_schema_draft():
    resp = client.get("/resources/schemas/icarAnimalCoreResource")
    schema = resp.json()
    assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
