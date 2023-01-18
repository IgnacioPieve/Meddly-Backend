from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

from tests.conftest import TestUser

body = {
    "first_name": "Ignacio",
    "last_name": "Pieve Roiger",
    "height": 170,
    "weight": 70,
    "sex": True,
    "birth": "2000-02-10T00:00:00",
    "phone": "+5493512345678",
}


def test_create_user(client: TestClient):
    response = client.post(
        "/user/", headers=TestUser(user_id="test").get_header(), json=body
    )
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]
    assert "id" in response.json()
    body["id"] = response.json()["id"]

    response = client.get("/user/", headers=TestUser(user_id="test").get_header())
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]


def test_update_user(client: TestClient):
    new_sex = False
    body["sex"] = new_sex
    response = client.post(
        "/user/", headers=TestUser(user_id="test").get_header(), json=body
    )
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]
