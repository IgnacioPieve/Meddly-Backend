from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient


def test_create_get_delete_notification_preference(client: TestClient):
    response = client.post(
        "/notification/preference", params={"notification_preference": "email"}
    )
    notifications = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert len(notifications) == 1
    assert "email" in notifications

    response = client.post(
        "/notification/preference", params={"notification_preference": "push"}
    )
    notifications = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert len(notifications) == 2
    assert "push" in notifications

    response = client.post(
        "/notification/preference", params={"notification_preference": "whatsapp"}
    )
    notifications = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert len(notifications) == 3
    assert "whatsapp" in notifications

    response = client.get("/notification/preference")
    notifications = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(notifications) == 3
    assert "email" in notifications
    assert "push" in notifications
    assert "whatsapp" in notifications

    response = client.delete(
        "/notification/preference", params={"notification_preference": "email"}
    )
    notifications = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(notifications) == 2
    assert "push" in notifications
    assert "whatsapp" in notifications

    response = client.delete(
        "/notification/preference", params={"notification_preference": "push"}
    )
    notifications = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(notifications) == 1
    assert "whatsapp" in notifications

    response = client.delete(
        "/notification/preference", params={"notification_preference": "whatsapp"}
    )
    notifications = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(notifications) == 0

    response = client.get("/notification/preference")
    notifications = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(notifications) == 0


def test_create_already_existing_notification_preference(client: TestClient):
    response = client.post(
        "/notification/preference", params={"notification_preference": "email"}
    )
    notifications = response.json()
    assert response.status_code == HTTP_201_CREATED
    assert len(notifications) == 1
    assert "email" in notifications

    response = client.post(
        "/notification/preference", params={"notification_preference": "email"}
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_delete_non_existing_notification_preference(client: TestClient):
    response = client.delete(
        "/notification/preference", params={"notification_preference": "whatsapp"}
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
