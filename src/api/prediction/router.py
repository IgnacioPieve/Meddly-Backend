from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile

from api.auth.dependencies import authenticate
from api.exceptions import GenericException
from api.prediction.schemas import (
    PredictionByImageSchema,
    PredictionBySymptomSchema,
    ProbabilitySchema,
)
from api.prediction.service import (
    get_predictions_by_image as get_predictions_by_image_service,
)
from api.prediction.service import (
    get_predictions_by_symptoms as get_predictions_by_symptoms_service,
)
from api.prediction.service import predict_by_image as predict_by_image_service
from api.prediction.service import predict_by_symptoms as predict_by_symptoms_service
from api.prediction.service import (
    verify_prediction_by_image as verify_prediction_by_image_service,
)
from api.prediction.service import (
    verify_prediction_by_symptom as verify_prediction_by_symptoms_service,
)
from api.user.models import User

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post(
    "/by_symptoms",
    response_model=list[ProbabilitySchema],
    status_code=200,
    summary="Prediction by symptoms",
)
async def predict_by_symptoms(
    symptoms_typed: list[str], user: User = Depends(authenticate)
):
    """
    # Prediction by symptoms

    Predicts the probability of a disease based on the symptoms provided.

    Args:
    - **symptoms_typed** (List[str]): List of symptoms codes (I.e: ['C123456789', 'C987654321']).
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **List[ProbabilitySchema]**: List of predicted probabilities for diseases.
    """

    try:
        return await predict_by_symptoms_service(symptoms_typed, user)
    except GenericException as e:
        raise e.http_exception


@router.get(
    "/by_symptoms",
    response_model=list[PredictionBySymptomSchema],
    status_code=200,
    summary="List all prediction by symptoms",
)
async def get_predictions_by_symptoms(
    start: datetime = None,
    page: int = 1,
    per_page: int = 10,
    user: User = Depends(authenticate),
):
    """
    # List all prediction by symptoms

    List all prediction by symptoms made by the user, sorted by date.

    Args:
    - **start** (datetime, optional): Start date for filtering predictions. Defaults to None.
    - **page** (int, optional): Page number for pagination. Defaults to 1.
    - **per_page** (int, optional): Number of predictions per page. Defaults to 10.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **List[PredictionBySymptomSchema]**: List of prediction results.
    """

    result = await get_predictions_by_symptoms_service(user, start, page, per_page)
    return result


@router.post(
    "/by_symptoms/verify/{prediction_id}",
    status_code=200,
    summary="Verify a prediction by symptoms",
)
async def verify_prediction_by_symptoms(
    prediction_id: int,
    real_disease: str,
    approval_to_save: bool = False,
    user=Depends(authenticate),
):
    """
    # Verify a prediction by symptoms

    Verifies a prediction by symptoms, providing the actual diagnosed disease code.
    The user can also provide consent to anonymously use their diagnosis for further retraining of the AI model.

    Args:
    - **prediction_id** (int): ID of the prediction to verify.
    - **real_disease** (str): The actual diagnosed disease code. (I.e: 'C123456789').
    - **approval_to_save** (bool, optional): Flag indicating whether the user consents to anonymously use their diagnosis for further retraining of the AI model.
                                          Defaults to False, indicating that the user does not provide consent to save their diagnosis for retraining.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.
    """

    try:
        await verify_prediction_by_symptoms_service(
            user, prediction_id, real_disease, approval_to_save
        )
    except GenericException as e:
        raise e.http_exception


@router.post(
    "/by_image",
    response_model=list[ProbabilitySchema],
    status_code=200,
    summary="Prediction by image",
)
async def predict_by_image(file: UploadFile, user: User = Depends(authenticate)):
    """
    # Prediction by image

    Predicts the probability of a disease based on an uploaded image.

    Args:
    - **file** (UploadFile): The image file to be uploaded.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **List[ProbabilitySchema]**: List of predicted probabilities for diseases.
    """

    result = await predict_by_image_service(file, user)
    return result


@router.get(
    "/by_image",
    response_model=list[PredictionByImageSchema],
    status_code=200,
    summary="List all prediction by image",
)
async def get_predictions_by_image(
    start: datetime = None,
    page: int = 1,
    per_page: int = 10,
    user: User = Depends(authenticate),
):
    """
    # List all prediction by image

    List all prediction by image made by the user, sorted by date.

    Args:
    - **start** (datetime, optional): Start date for filtering predictions. Defaults to None.
    - **page** (int, optional): Page number for pagination. Defaults to 1.
    - **per_page** (int, optional): Number of predictions per page. Defaults to 10.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **List[PredictionByImageSchema]**: List of prediction results.
    """

    result = await get_predictions_by_image_service(user, start, page, per_page)
    return result


@router.post(
    "/by_image/verify/{prediction_id}",
    status_code=200,
    summary="Verify a prediction by image",
)
async def verify_prediction_by_image(
    prediction_id: int,
    real_disease: str,
    approval_to_save: bool = False,
    user: User = Depends(authenticate),
):
    """
    # Verify a prediction by image

    Verifies a prediction by image, providing the actual diagnosed disease code.
    The user can also provide consent to anonymously use their diagnosis for further retraining of the AI model.

    Args:
    - **prediction_id** (int): ID of the prediction to verify.
    - **real_disease** (str): The actual diagnosed disease code. (I.e: 'C123456789').
    - **approval_to_save** (bool, optional): Flag indicating whether the user consents to anonymously use their diagnosis for further retraining of the AI model.
                                            Defaults to False, indicating that the user does not provide consent to save their diagnosis for retraining.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.
    """

    try:
        await verify_prediction_by_image_service(
            user, prediction_id, real_disease, approval_to_save
        )
    except GenericException as e:
        raise e.http_exception
