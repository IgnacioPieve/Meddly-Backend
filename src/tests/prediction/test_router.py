from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.testclient import TestClient


def test_create_get_verify_prediction_by_symptom(client: TestClient):
    symptom_codes = ["C0018681"]  # Headache
    real_disease = "C0021400"  # Flu

    response = client.post("/prediction/by_symptoms", json=symptom_codes)
    prediction = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(prediction) > 0
    original_predictions = [prediction]

    response = client.post("/prediction/by_symptoms", json=symptom_codes)
    prediction = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(prediction) > 0
    original_predictions.append(prediction)

    response = client.get("/prediction/by_symptoms")
    predictions = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(predictions) == 2
    prediction_ids = []
    for i in range(2):
        prediction = predictions[i]
        assert "C0018681" == prediction["symptoms"][0]["code"]
        assert prediction["verified"] == False
        assert prediction["real_disease"] is None
        assert prediction["prediction"] == original_predictions[i]
        assert "id" in prediction
        prediction_ids.append(prediction["id"])

    # Verify the first prediction with no approval to save
    response = client.post(
        f"/prediction/by_symptoms/verify/{prediction_ids[0]}",
        params={"real_disease": real_disease},
    )
    assert response.status_code == HTTP_200_OK

    # Verify the second prediction with approval to save
    response = client.post(
        f"/prediction/by_symptoms/verify/{prediction_ids[1]}",
        params={"real_disease": real_disease, "approval_to_save": True},
    )
    assert response.status_code == HTTP_200_OK

    response = client.get("/prediction/by_symptoms")
    predictions = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(predictions) == 2
    for i in range(2):
        prediction = predictions[i]
        assert "C0018681" == prediction["symptoms"][0]["code"]
        assert prediction["verified"] == True
        assert prediction["real_disease"] == real_disease
        assert prediction["prediction"] == original_predictions[i]
        assert "id" in prediction

    # Assert that we cannot verify the same prediction twice
    response = client.post(
        f"/prediction/by_symptoms/verify/{prediction_ids[0]}",
        params={"real_disease": real_disease},
    )
    assert response.status_code == HTTP_400_BAD_REQUEST

    response = client.post(
        f"/prediction/by_symptoms/verify/{prediction_ids[1]}",
        params={"real_disease": real_disease, "approval_to_save": True},
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_create_get_verify_prediction_by_image(client: TestClient):
    real_disease = "C0025202"  # Melanoma
    path = f"tests/prediction/test_image.jpg"

    with open(path, "rb") as file:
        response = client.post("/prediction/by_image", files={"file": file})
    prediction = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(prediction) > 0
    original_predictions = [prediction]

    with open(path, "rb") as file:
        response = client.post("/prediction/by_image", files={"file": file})
    prediction = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(prediction) > 0
    original_predictions.append(prediction)

    response = client.get("/prediction/by_image")
    predictions = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(predictions) == 2
    prediction_ids = []
    for i in range(2):
        prediction = predictions[i]
        assert prediction["verified"] == False
        assert prediction["real_disease"] is None
        assert prediction["prediction"] == original_predictions[i]
        assert "id" in prediction
        assert "image_name" in prediction
        request = client.get(f'/image/{prediction["image_name"]}')
        assert request.status_code == HTTP_200_OK
        prediction_ids.append(prediction["id"])

    # Verify the first prediction with no approval to save
    response = client.post(
        f"/prediction/by_image/verify/{prediction_ids[0]}",
        params={"real_disease": real_disease},
    )
    assert response.status_code == HTTP_200_OK

    # Verify the second prediction with approval to save
    response = client.post(
        f"/prediction/by_image/verify/{prediction_ids[1]}",
        params={"real_disease": real_disease, "approval_to_save": True},
    )
    assert response.status_code == HTTP_200_OK

    response = client.get("/prediction/by_image")
    predictions = response.json()
    assert response.status_code == HTTP_200_OK
    assert len(predictions) == 2
    for i in range(2):
        prediction = predictions[i]
        assert prediction["verified"] == True
        assert prediction["real_disease"] == real_disease
        assert prediction["prediction"] == original_predictions[i]
        assert "image_name" in prediction
        request = client.get(f'/image/{prediction["image_name"]}')
        assert request.status_code == HTTP_200_OK
        assert "id" in prediction

    # Assert that we cannot verify the same prediction twice
    response = client.post(
        f"/prediction/by_image/verify/{prediction_ids[0]}",
        params={"real_disease": real_disease},
    )
    assert response.status_code == HTTP_400_BAD_REQUEST

    response = client.post(
        f"/prediction/by_image/verify/{prediction_ids[1]}",
        params={"real_disease": real_disease, "approval_to_save": True},
    )
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_predict_by_unexisting_symptom(client: TestClient):
    symptom_codes = ["C0018681", "UNEXISTING"]  # Headache, unexisting symptom
    response = client.post("/prediction/by_symptoms", json=symptom_codes)
    assert response.status_code == HTTP_400_BAD_REQUEST


def test_verify_unexisting_prediction(client: TestClient):
    response = client.post(
        "/prediction/by_symptoms/verify/0", params={"real_disease": "C0021400"}
    )
    assert response.status_code == HTTP_400_BAD_REQUEST

    response = client.post(
        "/prediction/by_image/verify/0", params={"real_disease": "C0021400"}
    )
    assert response.status_code == HTTP_400_BAD_REQUEST
