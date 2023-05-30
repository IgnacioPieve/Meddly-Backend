from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient

"""
Checkear: 
    - medicamento fuera de fecha
    - medicamento de otra persona
    - medicamento con horas fuera de rango
    
    - consumo fuera de fecha (con fecha de fin y sin fecha de fin)
    - consumo de otra persona
    - consumos suman y restan stock
    - consumo
    
    - con fecha de fin
"""

base_body = {
    "name": "Ibuprofeno",
    "start_date": datetime.now().isoformat(),
    "stock": 18,
    "stock_warning": 5,
    "presentation": "Pastilla",
    "dosis_unit": "mg",
    "dosis": 1.5,
    "instructions": "Disolver la pastilla en agua",
}


# interval (2, 3, 4, 5) and hours or days [1, 2, 3, 4, 5, 6, 7] and hours or nothing


def test_create_get_delete_medicine(client: TestClient):
    # Create medicine with interval
    medicines_ids = []
    bodies = [
        {
            **base_body,
            "interval": 2,
            "hours": ["08:00", "11:30", "18:00"],
        },
        {
            **base_body,
            "days": [1, 3, 5, 7],
            "hours": ["08:00", "11:30", "18:00"],
        },
        {
            **base_body,
        },
        {
            "end_date": (datetime.now() + timedelta(days=2)).isoformat(),
            **base_body,
        },
    ]

    for body in bodies:
        response = client.post("/medicine/medicine", json=body)
        assert response.status_code == HTTP_201_CREATED
        medicine = response.json()
        assert "id" in medicine
        medicines_ids.append(medicine["id"])

    # Get medicines
    response = client.get("/medicine/medicine")
    assert response.status_code == HTTP_200_OK
    medicines = response.json()
    assert len(medicines) == len(bodies)
    for medicine in medicines:
        assert "id" in medicine
        assert medicine["id"] in medicines_ids

    # Delete medicines
    for medicine_id in medicines_ids:
        response = client.delete(f"/medicine/medicine/{medicine_id}")
        assert response.status_code == HTTP_200_OK

    # Check deletion
    response = client.get("/medicine/medicine")
    assert response.status_code == HTTP_200_OK
    medicines = response.json()
    assert len(medicines) == 0


def test_error_interval_and_days(client: TestClient):
    body = {
        **base_body,
        "interval": 2,
        "days": [1, 3, 5, 7],
        "hours": ["08:00", "11:30", "18:00"],
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 300


def test_error_no_hour_selected(client: TestClient):
    body = {
        **base_body,
        "interval": 2,
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 301


def test_error_incorrect_hour_format(client: TestClient):
    body = {
        **base_body,
        "interval": 2,
        "hours": ["08:00", "11:30", "18:00", "25:00"],
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 304


def test_delete_non_existent_medicine(client: TestClient):
    response = client.delete("/medicine/medicine/123456789")
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 305


def test_create_delete_consumption(client: TestClient):
    # Create medicine
    body = {
        **base_body,
        "interval": 2,
        "hours": ["08:00", "11:30", "18:00"],
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_201_CREATED
    medicine = response.json()
    assert "id" in medicine

    # Create consumption
    body = {
        "medicine_id": medicine["id"],
        "date": (
            (datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2))
            .replace(hour=8, minute=0, second=0, microsecond=0)
            .isoformat()
        ),
        "real_consumption_date": (
            datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2)
        ).isoformat(),
    }
    response = client.post("/medicine/consumption", json=body)
    assert response.status_code == HTTP_201_CREATED

    # Delete consumption
    response = client.post(f"/medicine/consumption_delete", json=body)
    assert response.status_code == HTTP_200_OK

    # Delete medicine
    response = client.delete(f"/medicine/medicine/{medicine['id']}")
    assert response.status_code == HTTP_200_OK


def test_error_create_consumption_with_non_existent_medicine(client: TestClient):
    body = {
        "medicine_id": "123456789",
        "date": datetime.now().isoformat(),
        "real_consumption_date": datetime.now().isoformat(),
    }
    response = client.post("/medicine/consumption", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 305


def test_error_consumption_already_exists(client: TestClient):
    # Create medicine
    body = {
        **base_body,
        "interval": 2,
        "hours": ["08:00", "11:30", "18:00"],
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_201_CREATED
    medicine = response.json()
    assert "id" in medicine

    # Create consumption
    body = {
        "medicine_id": medicine["id"],
        "date": (
            (datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2))
            .replace(hour=8, minute=0, second=0, microsecond=0)
            .isoformat()
        ),
        "real_consumption_date": (
            datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2)
        ).isoformat(),
    }
    response = client.post("/medicine/consumption", json=body)
    assert response.status_code == HTTP_201_CREATED

    # Create consumption again
    response = client.post("/medicine/consumption", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 306

    # Delete consumption
    response = client.post(f"/medicine/consumption_delete", json=body)
    assert response.status_code == HTTP_200_OK

    # Delete medicine
    response = client.delete(f"/medicine/medicine/{medicine['id']}")
    assert response.status_code == HTTP_200_OK


def test_delete_non_existent_consumption(client: TestClient):
    # Create medicine
    body = {
        **base_body,
        "interval": 2,
        "hours": ["08:00", "11:30", "18:00"],
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_201_CREATED
    medicine = response.json()
    assert "id" in medicine

    body = {
        "medicine_id": medicine["id"],
        "date": (
            (datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2))
            .replace(hour=8, minute=0, second=0, microsecond=0)
            .isoformat()
        ),
        "real_consumption_date": (
            datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2)
        ).isoformat(),
    }
    response = client.post("/medicine/consumption_delete", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 307


def test_delecte_consumption_with_non_existent_medicine(client: TestClient):
    body = {
        "medicine_id": "123456789",
        "date": datetime.now().isoformat(),
        "real_consumption_date": datetime.now().isoformat(),
    }
    response = client.post("/medicine/consumption_delete", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 305


def test_create_consumption_for_medicine_with_no_day_nor_interval(client: TestClient):
    # Create medicine
    body = base_body
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_201_CREATED
    medicine = response.json()
    assert "id" in medicine

    # Create consumption
    body = {
        "medicine_id": medicine["id"],
        "date": (
            (datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2))
            .replace(hour=8, minute=0, second=0, microsecond=0)
            .isoformat()
        ),
        "real_consumption_date": (
            datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2)
        ).isoformat(),
    }
    response = client.post("/medicine/consumption", json=body)
    assert response.status_code == HTTP_201_CREATED

    # Delete consumption
    response = client.post(f"/medicine/consumption_delete", json=body)
    assert response.status_code == HTTP_200_OK

    # Delete medicine
    response = client.delete(f"/medicine/medicine/{medicine['id']}")
    assert response.status_code == HTTP_200_OK


def test_create_consumption_with_invalid_date(client: TestClient):
    # Create medicine
    body = {
        **base_body,
        "interval": 2,
        "hours": ["08:00", "11:30", "18:00"],
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_201_CREATED
    medicine = response.json()
    assert "id" in medicine

    # Create consumption
    body = {
        "medicine_id": medicine["id"],
        "date": (
            (datetime.fromisoformat(medicine["start_date"]) + timedelta(days=1))
            .replace(hour=11, minute=30, second=0, microsecond=0)
            .isoformat()
        ),
        "real_consumption_date": (
            datetime.fromisoformat(medicine["start_date"]) + timedelta(days=3)
        ).isoformat(),
    }
    response = client.post("/medicine/consumption", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 302

    # Delete medicine
    response = client.delete(f"/medicine/medicine/{medicine['id']}")
    assert response.status_code == HTTP_200_OK


def test_create_consumption_with_invalid_hour(client: TestClient):
    # Create medicine
    body = {
        **base_body,
        "interval": 2,
        "hours": ["08:00", "11:30", "18:00"],
    }
    response = client.post("/medicine/medicine", json=body)
    assert response.status_code == HTTP_201_CREATED
    medicine = response.json()
    assert "id" in medicine

    # Create consumption
    body = {
        "medicine_id": medicine["id"],
        "date": (
            (datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2))
            .replace(hour=11, minute=35, second=0, microsecond=0)
            .isoformat()
        ),
        "real_consumption_date": (
            datetime.fromisoformat(medicine["start_date"]) + timedelta(days=2)
        ).isoformat(),
    }
    response = client.post("/medicine/consumption", json=body)
    assert response.status_code == HTTP_400_BAD_REQUEST
    assert response.json()["detail"]["code"] == 303

    # Delete medicine
    response = client.delete(f"/medicine/medicine/{medicine['id']}")
    assert response.status_code == HTTP_200_OK
