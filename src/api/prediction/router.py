from datetime import datetime

from fastapi import APIRouter, Depends, UploadFile

from api.auth.dependencies import authenticate
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
from api.prediction.service import verify_prediction_by_image as verify_prediction_by_image_service
from api.prediction.service import verify_prediction_by_symptom as verify_prediction_by_symptoms_service
from api.prediction.service import predict_by_image as predict_by_image_service
from api.prediction.service import predict_by_symptoms as predict_by_symptoms_service
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
    result = await predict_by_symptoms_service(symptoms_typed, user)
    return result


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
    await verify_prediction_by_symptoms_service(user, prediction_id, real_disease, approval_to_save)


@router.post(
    "/by_image",
    response_model=list[ProbabilitySchema],
    status_code=200,
    summary="Prediction by image",
)
async def predict_by_image(file: UploadFile, user: User = Depends(authenticate)):
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
    await verify_prediction_by_image_service(
        user,
        prediction_id,
        real_disease,
        approval_to_save
    )
