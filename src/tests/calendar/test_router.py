from datetime import datetime, timedelta

from starlette.status import HTTP_200_OK, HTTP_201_CREATED
from starlette.testclient import TestClient


def test_get_empty_calendar(client: TestClient):
    response = client.get("/calendar")
    assert response.status_code == HTTP_200_OK
    calendar = response.json()
    assert "appointments" in calendar["test_user"]
    assert "measurements" in calendar["test_user"]
    assert "consumptions" in calendar["test_user"]
    assert len(calendar["test_user"]["appointments"]) == 0
    assert len(calendar["test_user"]["measurements"]) == 0
    assert len(calendar["test_user"]["consumptions"]) == 0


def test_appointments(client: TestClient):
    base_appointment = {
        "name": "Consulta con Cardiólogo",
        "doctor": "Dr. Juan Perez",
        "speciality": "Cardiología",
        "location": "Hospital de la ciudad",
        "notes": "Llevar los resultados de los análisis",
    }
    appointments = [
        {**base_appointment, "date": (datetime.now() - timedelta(days=30)).isoformat()},
        {**base_appointment, "date": (datetime.now() - timedelta(days=20)).isoformat()},
        {**base_appointment, "date": (datetime.now() - timedelta(days=10)).isoformat()},
        {**base_appointment, "date": (datetime.now()).isoformat()},
        {**base_appointment, "date": (datetime.now() + timedelta(days=10)).isoformat()},
        {**base_appointment, "date": (datetime.now() + timedelta(days=20)).isoformat()},
        {**base_appointment, "date": (datetime.now() + timedelta(days=30)).isoformat()},
    ]

    base_measurement = {
        "type": "Glucosa",
        "value": 95.0,
        "unit": "mg/dl",
    }
    measurements = [
        {**base_measurement, "date": (datetime.now() - timedelta(days=30)).isoformat()},
        {**base_measurement, "date": (datetime.now() - timedelta(days=20)).isoformat()},
        {**base_measurement, "date": (datetime.now() - timedelta(days=10)).isoformat()},
        {**base_measurement, "date": (datetime.now()).isoformat()},
        {**base_measurement, "date": (datetime.now() + timedelta(days=10)).isoformat()},
        {**base_measurement, "date": (datetime.now() + timedelta(days=20)).isoformat()},
        {**base_measurement, "date": (datetime.now() + timedelta(days=30)).isoformat()},
    ]

    base_medicine = {
        "name": "Ibuprofeno",
        "stock": 18,
        "stock_warning": 5,
        "presentation": "Pastilla",
        "dosis_unit": "mg",
        "dosis": 1.5,
        "instructions": "Disolver la pastilla en agua",
        "interval": 2,
        "hours": ["08:00", "11:30", "18:00"],
    }

    medicines = [
        {
            **base_medicine,
            "start_date": (datetime.now() - timedelta(days=30)).isoformat(),
            "end_date": datetime.now().isoformat(),
        },
        {
            **base_medicine,
            "start_date": datetime.now().isoformat(),
        },
        {
            **base_medicine,
            "start_date": datetime.now().isoformat(),
            "end_date": (datetime.now() + timedelta(days=30)).isoformat(),
        },
        {
            **base_medicine,
            "start_date": datetime.now().isoformat(),
            "interval": None,
            "hours": None,
        },
        {
            **base_medicine,
            "start_date": datetime.now().isoformat(),
            "interval": None,
            "days": [1, 2, 3, 4, 5, 6, 7],
        },
    ]

    for appointment in appointments:
        response = client.post("/appointment", json=appointment)
        assert response.status_code == HTTP_201_CREATED
        assert "id" in response.json()

    for measurement in measurements:
        response = client.post("/measurement", json=measurement)
        assert response.status_code == HTTP_201_CREATED
        assert "id" in response.json()

    medicines_ids = []
    for medicine in medicines:
        response = client.post("/medicine/medicine", json=medicine)
        medicine = response.json()
        assert response.status_code == HTTP_201_CREATED
        assert "id" in medicine
        medicines_ids.append(medicine["id"])

    consumptions = [
        {
            "medicine_id": medicines_ids[0],
            "date": (datetime.now() - timedelta(days=28))
            .replace(hour=11, minute=30)
            .isoformat(),
            "real_consumption_date": (datetime.now() - timedelta(days=28))
            .replace(hour=11, minute=30)
            .isoformat(),
        },
        {
            "medicine_id": medicines_ids[0],
            "date": (datetime.now() - timedelta(days=26))
            .replace(hour=11, minute=30)
            .isoformat(),
            "real_consumption_date": (datetime.now() - timedelta(days=26))
            .replace(hour=11, minute=30)
            .isoformat(),
        },
        {
            "medicine_id": medicines_ids[1],
            "date": (datetime.now() + timedelta(days=2))
            .replace(hour=11, minute=30)
            .isoformat(),
            "real_consumption_date": (datetime.now() + timedelta(days=2))
            .replace(hour=11, minute=30)
            .isoformat(),
        },
        {
            "medicine_id": medicines_ids[2],
            "date": (datetime.now() + timedelta(days=2))
            .replace(hour=11, minute=30)
            .isoformat(),
            "real_consumption_date": (datetime.now() + timedelta(days=2))
            .replace(hour=11, minute=30)
            .isoformat(),
        },
        {
            "medicine_id": medicines_ids[2],
            "date": (datetime.now() + timedelta(days=4))
            .replace(hour=11, minute=30)
            .isoformat(),
            "real_consumption_date": (datetime.now() + timedelta(days=4))
            .replace(hour=11, minute=30)
            .isoformat(),
        },
        {
            "medicine_id": medicines_ids[3],
            "date": (datetime.now() + timedelta(days=4))
            .replace(hour=11, minute=30)
            .isoformat(),
            "real_consumption_date": (datetime.now() + timedelta(days=4))
            .replace(hour=11, minute=30)
            .isoformat(),
        },
    ]
    for consumption in consumptions:
        response = client.post("/medicine/consumption", json=consumption)
        assert response.status_code == HTTP_201_CREATED

    response = client.get("/calendar")
    assert response.status_code == HTTP_200_OK
    calendar = response.json()
    assert "appointments" in calendar["test_user"]
    assert "measurements" in calendar["test_user"]
    assert "consumptions" in calendar["test_user"]
    assert len(calendar["test_user"]["appointments"]) == 3
    assert len(calendar["test_user"]["measurements"]) == 3
    # TODO: Check this
    # assert len(calendar["test_user"]["consumptions"]) == 103
