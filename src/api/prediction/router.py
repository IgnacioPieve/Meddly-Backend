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
async def get_predictions_by_symptoms(user: User = Depends(authenticate)):
    result = await get_predictions_by_symptoms_service(user)
    print(type(result[0].prediction))
    return result


# @router.post(
#     "/by_symptoms/verify/{prediction_id}",
#     status_code=200,
#     include_in_schema=False,
# )
# @router.post(
#     "/by_symptoms/verify/{prediction_id}/",
#     status_code=200,
#     summary="Verify a prediction by symptoms",
# )
# def verify_prediction_by_symptoms(
#     prediction_id: int,
#     real_disease: str,
#     approval_to_save: bool = False,
#     authentication=Depends(authenticate),
# ):
#     user, db = authentication
#     prediction = PredictionBySymptom(
#         db,
#         PredictionBySymptom.id == prediction_id,
#         PredictionBySymptom.user_id == user.id,
#     ).get()
#     if not prediction:
#         raise_errorcode(702)
#     prediction.verify(real_disease, approval_to_save)


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
async def get_predictions_by_image(user: User = Depends(authenticate)):
    result = await get_predictions_by_image_service(user)
    return result


# @router.post(
#     "/by_image/verify/{prediction_id}",
#     status_code=200,
#     include_in_schema=False,
# )
# @router.post(
#     "/by_image/verify/{prediction_id}/",
#     status_code=200,
#     summary="Verify a prediction by image",
# )
# def verify_prediction_by_image(
#     prediction_id: str,
#     real_disease: str,
#     approval_to_save: bool = False,
#     authentication=Depends(authenticate),
# ):
#     user, db = authentication
#
#     prediction = PredictionByImage(
#         db, PredictionByImage.user_id == user.id, PredictionByImage.id == prediction_id
#     ).get()
#     if prediction is None:
#         raise_errorcode(702)
#     prediction.verify(real_disease, approval_to_save)
