from fastapi import APIRouter, Depends, UploadFile
from PIL import Image

from auth.dependencies import authenticate
from image.models import Image as ImageModel
from models import raise_errorcode
from prediction.models.by_image import PredictionByImage
from prediction.models.by_symptom import PredictionBySymptom
from prediction.schemas import (
    PredictionByImageSchema,
    PredictionBySymptomSchema,
    ProbabilitySchema,
)

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post(
    "/by_symptoms",
    response_model=list[ProbabilitySchema],
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "/by_symptoms/",
    response_model=list[ProbabilitySchema],
    status_code=200,
    summary="Prediction by symptoms",
)
def symptom_prediction(symptoms_typed: list[str], authentication=Depends(authenticate)):
    user, db = authentication
    return PredictionBySymptom(db, user=user).predict(symptoms_typed)


@router.get(
    "/by_symptoms",
    response_model=list[PredictionBySymptomSchema],
    status_code=200,
    include_in_schema=False,
)
@router.get(
    "/by_symptoms/",
    response_model=list[PredictionBySymptomSchema],
    status_code=200,
    summary="List all prediction by symptoms",
)
def symptom_prediction_list(authentication=Depends(authenticate)):
    user, _ = authentication
    return user.predictions_by_symptoms


@router.post(
    "/by_symptoms/verify/{prediction_id}",
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "/by_symptoms/verify/{prediction_id}/",
    status_code=200,
    summary="Verify a prediction by symptoms",
)
def verify_prediction_by_symptoms(
    prediction_id: int,
    real_disease: str,
    approval_to_save: bool = False,
    authentication=Depends(authenticate),
):
    user, db = authentication
    prediction = PredictionBySymptom(
        db,
        PredictionBySymptom.id == prediction_id,
        PredictionBySymptom.user_id == user.id,
    ).get()
    if not prediction:
        raise_errorcode(702)
    prediction.verify(real_disease, approval_to_save)


@router.post(
    "/by_image",
    response_model=list[ProbabilitySchema],
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "/by_image/",
    response_model=list[ProbabilitySchema],
    status_code=200,
    summary="Prediction by image",
)
def image_prediction(file: UploadFile, authentication=Depends(authenticate)):
    user, db = authentication

    image = ImageModel(db, user=user, tag="prediction_by_image")
    image.set_image(Image.open(file.file).resize((512, 512)))
    image.create()

    return PredictionByImage(db, user=user, image=image).predict(file)


@router.get(
    "/by_image",
    response_model=list[PredictionByImageSchema],
    status_code=200,
    include_in_schema=False,
)
@router.get(
    "/by_image/",
    response_model=list[PredictionByImageSchema],
    status_code=200,
    summary="List all prediction by image",
)
def image_prediction_list(authentication=Depends(authenticate)):
    user, _ = authentication
    return user.predictions_by_image


@router.post(
    "/by_image/verify/{prediction_id}",
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "/by_image/verify/{prediction_id}/",
    status_code=200,
    summary="Verify a prediction by image",
)
def verify_prediction_by_image(
    prediction_id: str,
    real_disease: str,
    approval_to_save: bool = False,
    authentication=Depends(authenticate),
):
    user, db = authentication

    prediction = PredictionByImage(
        db, PredictionByImage.user_id == user.id, PredictionByImage.id == prediction_id
    ).get()
    if prediction is None:
        raise_errorcode(702)
    prediction.verify(real_disease, approval_to_save)
