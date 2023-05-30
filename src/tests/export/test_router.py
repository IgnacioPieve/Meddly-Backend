from starlette.testclient import TestClient


def test_export_pdf(client: TestClient):
    response = client.get("/export/export_pdf")
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
