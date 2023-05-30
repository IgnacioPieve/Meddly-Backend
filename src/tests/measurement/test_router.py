import datetime

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

body = {
    "type": "Glucosa",
    "value": 95.0,
    "unit": "mg/dl",
    "date": datetime.datetime.now().isoformat(),
}


def test_create_get_update_delete_measurement(client: TestClient):
    # The happy path

    # Create
    response = client.post("/measurement", json=body)
    assert response.status_code == HTTP_201_CREATED
    measurement = response.json()
    for value in body:
        assert body[value] == measurement[value]
    assert "id" in measurement
    measurement_id = measurement["id"]

    # Get
    response = client.get(f"/measurement")
    assert response.status_code == HTTP_200_OK
    measurements = response.json()
    measurement_exists = False
    for measurement in measurements:
        if measurement["id"] == measurement_id:
            measurement_exists = True
            for value in body:
                assert body[value] == measurement[value]
            break
    assert measurement_exists

    # Update
    body["value"] = 90.0
    response = client.post(f"/measurement/{measurement_id}", json=body)
    assert response.status_code == HTTP_200_OK
    measurement = response.json()
    for value in body:
        assert body[value] == measurement[value]
    assert "id" in measurement
    assert measurement_id == measurement["id"]

    # Delete
    response = client.delete(f"/measurement/{measurement_id}")
    assert response.status_code == HTTP_200_OK
    response = client.get(f"/measurement")
    assert response.status_code == HTTP_200_OK
    measurements = response.json()
    assert len(measurements) == 0


def test_update_non_existent_measurement(client: TestClient):
    # Update
    body["value"] = 90.0
    response = client.post(f"/measurement/1", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_delete_non_existent_measurement(client: TestClient):
    # Delete
    response = client.delete(f"/measurement/1")
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_get_with_date_range(client: TestClient):
    # Create
    response = client.post("/measurement", json=body)
    assert response.status_code == HTTP_201_CREATED
    measurement = response.json()
    for value in body:
        assert body[value] == measurement[value]
    assert "id" in measurement
    measurement_id = measurement["id"]

    # Successfull get
    start = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    end = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
    response = client.get(f"/measurement?start={start}&end={end}")
    assert response.status_code == HTTP_200_OK
    measurements = response.json()
    assert len(measurements) == 1
    assert measurements[0]["id"] == measurement_id

    # Unsuccessfull get
    start = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    end = (datetime.datetime.now() - datetime.timedelta(days=6)).isoformat()
    response = client.get(f"/measurement?start={start}&end={end}")
    assert response.status_code == HTTP_200_OK
    measurements = response.json()
    assert len(measurements) == 0
