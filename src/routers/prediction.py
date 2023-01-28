from fastapi import APIRouter, Depends, UploadFile
from PIL import Image

from dependencies import auth
from models.image import Image as ImageModel
from models.predictions.by_image import PredictionByImage
from models.predictions.by_symptom import PredictionBySymptom
from schemas.prediction import (PredictionByImageSchema,
                                PredictionBySymptomSchema, ProbabilitySchema)
from schemas.utils import SearchResultSchema

router = APIRouter(prefix="/prediction", tags=["Predictions"])


@router.post(
    "symptom",
    response_model=SearchResultSchema,
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "symptom/",
    response_model=SearchResultSchema,
    status_code=200,
    summary="Symptoms Search",
)
def symptom_search(symptom: str, authentication=Depends(auth.authenticate)):
    """
    symptom_search
    """
    _, _ = authentication
    return PredictionBySymptom.search(symptom)


@router.post(
    "symptom/prediction",
    response_model=list[ProbabilitySchema],
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "symptom/prediction/",
    response_model=list[ProbabilitySchema],
    status_code=200,
    summary="Prediction by symptoms",
)
def symptom_prediction(
        symptoms_typed: list[str], authentication=Depends(auth.authenticate)
):
    user, db = authentication
    return PredictionBySymptom(db, user=user).predict(symptoms_typed)


@router.post(
    "image/prediction",
    response_model=list[ProbabilitySchema],
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "image/prediction/",
    response_model=list[ProbabilitySchema],
    status_code=200,
    summary="Prediction by image",
)
def image_prediction(
        file: UploadFile, authentication=Depends(auth.authenticate)
):
    user, db = authentication

    image = ImageModel(db, user=user)
    image.set_image(Image.open(file.file).resize((512, 512)))
    image.create()

    return PredictionByImage(db, user=user, image=image).predict(file)


@router.get(
    "symptom/prediction",
    response_model=list[PredictionBySymptomSchema],
    status_code=200,
    include_in_schema=False,
)
@router.get(
    "symptom/prediction/",
    response_model=list[PredictionBySymptomSchema],
    status_code=200,
    summary="List all predictions by symptoms",
)
def symptom_prediction(
        authentication=Depends(auth.authenticate)
):
    user, _ = authentication
    return user.predictions_by_symptom


@router.get(
    "image/prediction",
    response_model=list[PredictionByImageSchema],
    status_code=200,
    include_in_schema=False,
)
@router.get(
    "image/prediction/",
    response_model=list[PredictionByImageSchema],
    status_code=200,
    summary="List all predictions by image",
)
def image_prediction(
        authentication=Depends(auth.authenticate)
):
    user, _ = authentication
    return user.predictions_by_image
