import datetime

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

body = {
    "name": "Consulta con Cardiólogo",
    "doctor": "Dr. Juan Perez",
    "speciality": "Cardiología",
    "location": "Hospital de la ciudad",
    "notes": "Llevar los resultados de los análisis",
    "date": datetime.datetime.now().isoformat(),
}


def test_create_get_update_delete_appointment(client: TestClient):
    # The happy path

    # Create
    response = client.post("/appointment", json=body)
    assert response.status_code == HTTP_201_CREATED
    appointment = response.json()
    for value in body:
        assert body[value] == appointment[value]
    assert "id" in appointment
    appointment_id = appointment["id"]

    # Get
    response = client.get(f"/appointment")
    assert response.status_code == HTTP_200_OK
    appointments = response.json()
    appointment_exists = False
    for appointment in appointments:
        if appointment["id"] == appointment_id:
            appointment_exists = True
            for value in body:
                assert body[value] == appointment[value]
            break
    assert appointment_exists

    # Update
    body["name"] = "Consulta de Cardiología"
    response = client.post(f"/appointment/{appointment_id}", json=body)
    assert response.status_code == HTTP_200_OK
    appointment = response.json()
    for value in body:
        assert body[value] == appointment[value]
    assert "id" in appointment
    assert appointment_id == appointment["id"]

    # Delete
    response = client.delete(f"/appointment/{appointment_id}")
    assert response.status_code == HTTP_200_OK
    response = client.get(f"/appointment")
    assert response.status_code == HTTP_200_OK
    appointments = response.json()
    assert len(appointments) == 0


def test_update_non_existent_appointment(client: TestClient):
    # Update
    body["name"] = "Consulta de Cardiología"
    response = client.post(f"/appointment/1", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_delete_non_existent_appointment(client: TestClient):
    # Delete
    response = client.delete(f"/appointment/1")
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_get_with_date_range(client: TestClient):
    # Create
    response = client.post("/appointment", json=body)
    assert response.status_code == HTTP_201_CREATED
    appointment = response.json()
    for value in body:
        assert body[value] == appointment[value]
    assert "id" in appointment
    appointment_id = appointment["id"]

    # Successfull get
    start = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
    end = (datetime.datetime.now() + datetime.timedelta(days=1)).isoformat()
    response = client.get(f"/appointment?start={start}&end={end}")
    assert response.status_code == HTTP_200_OK
    appointments = response.json()
    assert len(appointments) == 1
    assert appointments[0]["id"] == appointment_id

    # Unsuccessfull get
    start = (datetime.datetime.now() - datetime.timedelta(days=7)).isoformat()
    end = (datetime.datetime.now() - datetime.timedelta(days=6)).isoformat()
    response = client.get(f"/appointment?start={start}&end={end}")
    assert response.status_code == HTTP_200_OK
    appointments = response.json()
    assert len(appointments) == 0
