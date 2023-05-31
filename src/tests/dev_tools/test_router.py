from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient


def test_endpoints(client: TestClient):
    endpoints = [
        {"method": "post", "endpoint": "/get-some-users"},
        {"method": "get", "endpoint": "/status"},
        {"method": "post", "endpoint": "/reset-database"},
        {"method": "post", "endpoint": "/load-example-data"},
    ]
    for endpoint in endpoints:
        response = getattr(client, endpoint["method"])(f"/dev{endpoint['endpoint']}")
        assert response.status_code == HTTP_200_OK
