from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

body = {
    "first_name": "Ignacio",
    "last_name": "Pieve Roiger",
    "height": 170,
    "weight": 70,
    "sex": True,
    "birth": "2000-02-10T00:00:00",
    "phone": "+5493512345678",
}


def test_get_user(client: TestClient):
    user = client.get("/user")
    assert user.status_code == HTTP_200_OK


def test_update_user(client: TestClient):
    response = client.post("/user", json=body)
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]
    assert "id" in response.json()
    body["id"] = response.json()["id"]

    response = client.get("/user/")
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]
