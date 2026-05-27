from fastapi.testclient import TestClient

from app.main import app
from app.database import drop_all

client = TestClient(app)


def setup_function():
    drop_all()


def test_create_animal():
    payload = {
        "identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "specie": "Cattle",
        "gender": "Female",
    }
    resp = client.post("/animals", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["payload"]["specie"] == "Cattle"


def test_create_animal_duplicate():
    payload = {
        "identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "specie": "Cattle",
        "gender": "Female",
    }
    client.post("/animals", json=payload)
    resp = client.post("/animals", json=payload)
    assert resp.status_code == 409


def test_get_animal():
    payload = {
        "identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "specie": "Cattle",
        "gender": "Female",
    }
    client.post("/animals", json=payload)
    resp = client.get("/animals/es.magrama.bovine/ES091234567890")
    assert resp.status_code == 200
    assert resp.json()["payload"]["identifier"]["id"] == "ES091234567890"


def test_get_animal_not_found():
    resp = client.get("/animals/es.magrama.bovine/FAKE")
    assert resp.status_code == 404


def test_delete_animal():
    payload = {
        "identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "specie": "Cattle",
        "gender": "Female",
    }
    client.post("/animals", json=payload)
    resp = client.delete("/animals/es.magrama.bovine/ES091234567890")
    assert resp.status_code == 200
    resp = client.get("/animals/es.magrama.bovine/ES091234567890")
    assert resp.status_code == 404
