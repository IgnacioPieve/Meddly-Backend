from fastapi import APIRouter, Depends, UploadFile

from dependencies import auth
from models.utils import raise_errorcode
from routers.predictors.by_image.predictor import predict as predict_by_image
from routers.predictors.by_symptom.predictor import \
    predict as predict_by_symptom
from routers.predictors.by_symptom.predictor import search, symptoms
from schemas.utils import ProbabilitySchema, SearchResultSchema

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
    return search(symptom)


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
    _, _ = authentication
    for symptom in symptoms_typed:
        if symptom not in symptoms:
            raise_errorcode(700)
    return predict_by_symptom(symptoms_typed)


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
    _, _ = authentication
    return predict_by_image(file)
