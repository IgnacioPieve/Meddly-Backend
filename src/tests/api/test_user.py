from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient

body = {
    "name": "John Doe",
    "height": 1.70,
    "weight": 67,
    "sex": "M",
    "avatar": "avatar1",
}


def test_create_user(client: TestClient):
    response = client.post("/user/", headers={"cred": "test"}, json=body)
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]


def test_get_user(client: TestClient):
    response = client.get("/user/", headers={"cred": "test"})
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]


def test_update_user(client: TestClient):
    new_sex = "F"
    body["sex"] = new_sex
    response = client.post("/user/", headers={"cred": "test"}, json=body)
    assert response.status_code == HTTP_200_OK
    for value in body:
        assert body[value] == response.json()[value]
