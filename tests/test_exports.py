from fastapi.testclient import TestClient

from app.main import app
from app.database import drop_all

client = TestClient(app)


def setup_function():
    drop_all()


def _seed_data():
    client.post("/animals", json={
        "identifier": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "specie": "Cattle",
        "gender": "Female",
        "location": {"scheme": "es.rea", "id": "ES430000001"},
    })
    client.post("/resources", json={
        "resourceType": "icarWeightEventResource",
        "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "eventDateTime": "2026-03-15T08:30:00Z",
        "location": {"scheme": "es.rea", "id": "ES430000001"},
    })
    client.post("/locations", json={
        "identifier": {"scheme": "es.rea", "id": "ES430000001"},
        "name": "La Vega",
    })


def test_export_json_all():
    _seed_data()
    resp = client.get("/exports/json")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 3
    assert resp.headers.get("content-disposition") == "attachment; filename=export.json"


def test_export_json_filter_by_type():
    _seed_data()
    resp = client.get("/exports/json?resourceType=icarAnimalCoreResource")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["resourceType"] == "icarAnimalCoreResource"


def test_export_json_filter_by_location():
    _seed_data()
    resp = client.get("/exports/json?locationScheme=es.rea&locationId=ES430000001")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 2


def test_export_json_empty():
    resp = client.get("/exports/json")
    assert resp.status_code == 200
    assert resp.json() == []


def test_export_geojson_structure():
    _seed_data()
    resp = client.get("/exports/geojson")
    assert resp.status_code == 200
    geojson = resp.json()
    assert geojson["type"] == "FeatureCollection"
    assert "features" in geojson
    assert len(geojson["features"]) >= 3
    assert resp.headers.get("content-disposition") == "attachment; filename=export.geojson"
    assert resp.headers.get("content-type") == "application/geo+json"


def test_export_geojson_feature_properties():
    _seed_data()
    resp = client.get("/exports/geojson?resourceType=icarAnimalCoreResource")
    geojson = resp.json()
    feature = geojson["features"][0]
    assert feature["type"] == "Feature"
    props = feature["properties"]
    assert props["resourceType"] == "icarAnimalCoreResource"
    assert "internalId" in props
    assert feature["geometry"] is None


def test_export_geojson_with_coordinates():
    resp = client.post("/resources", json={
        "resourceType": "icarPositionObservationEventResource",
        "animal": {"scheme": "es.magrama.bovine", "id": "ES091234567890"},
        "eventDateTime": "2026-03-15T10:00:00Z",
        "latitude": 41.3874,
        "longitude": 2.1686,
    })
    assert resp.status_code == 200

    resp = client.get("/exports/geojson")
    geojson = resp.json()
    features = [f for f in geojson["features"] if f["properties"]["resourceType"] == "icarPositionObservationEventResource"]
    assert len(features) == 1
    feature = features[0]
    assert feature["geometry"]["type"] == "Point"
    assert feature["geometry"]["coordinates"] == [2.1686, 41.3874]


def test_export_geojson_filter_by_date():
    _seed_data()
    resp = client.get("/exports/geojson?fromDate=2026-01-01&toDate=2026-12-31")
    assert resp.status_code == 200
    geojson = resp.json()
    assert len(geojson["features"]) >= 1


def test_export_geojson_empty():
    resp = client.get("/exports/geojson")
    assert resp.status_code == 200
    geojson = resp.json()
    assert geojson["type"] == "FeatureCollection"
    assert geojson["features"] == []
