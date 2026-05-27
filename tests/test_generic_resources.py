from fastapi.testclient import TestClient

from app.main import app
from app.database import drop_all

client = TestClient(app)


def setup_function():
    drop_all()


VALID_ANIMAL = {
    "resourceType": "icarAnimalCoreResource",
    "identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
    "specie": "Cattle",
    "gender": "Female",
}


def test_create_resource():
    resp = client.post("/resources", json=VALID_ANIMAL)
    assert resp.status_code == 200


def test_create_resource_missing_type():
    resp = client.post("/resources", json={"specie": "Cattle"})
    assert resp.status_code == 422


def test_get_resource_types():
    resp = client.get("/resources/resource-types")
    assert resp.status_code == 200
    assert "resource_types" in resp.json()


def test_list_resources():
    client.post("/resources", json=VALID_ANIMAL)
    resp = client.get("/resources?resourceType=icarAnimalCoreResource")
    assert resp.status_code == 200
    assert resp.json()["total"] >= 1


def test_delete_resource():
    resp = client.post("/resources", json=VALID_ANIMAL)
    internal_id = resp.json()["internalId"]
    resp = client.delete(
        f"/resources/{internal_id}?resourceType=icarAnimalCoreResource"
    )
    assert resp.status_code == 200
    resp = client.get(f"/resources/{internal_id}?resourceType=icarAnimalCoreResource")
    assert resp.status_code == 404
