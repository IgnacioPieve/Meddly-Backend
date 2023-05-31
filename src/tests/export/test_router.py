from starlette.status import HTTP_200_OK
from starlette.testclient import TestClient


def test_export_pdf(client: TestClient):
    response = client.get("/export/export_pdf")
    assert response.status_code == HTTP_200_OK
    assert response.headers["Content-Type"] == "application/pdf"
