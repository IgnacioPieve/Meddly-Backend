

from fastapi import APIRouter, Depends

from auth.dependencies import authenticate
from prediction.models.by_symptom import PredictionBySymptom
from search.serializers import SearchResultSchema
from user_calendar.models.medicine import Medicine

router = APIRouter(prefix="/search", tags=["Search"])


@router.post(
    "/symptom_search",
    response_model=list[SearchResultSchema],
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "/symptom_search/",
    response_model=list[SearchResultSchema],
    status_code=200,
    summary="Symptoms Search",
)
def symptom_search(
    symptom: str, language: str = "es", authentication=Depends(authenticate)
):
    """
    symptom_search
    """
    _, _ = authentication
    # TODO: @ignacio.pieve This method should be moved to this folder
    return PredictionBySymptom.search(symptom, language)


@router.get(
    "/medicine_search",
    response_model=list[SearchResultSchema],
    status_code=200,
    include_in_schema=False,
)
@router.get(
    "/medicine_search/",
    response_model=list[SearchResultSchema],
    status_code=200,
    summary="Find medicine names",
)
def medicine_search(
    medicine_name: str,
    authentication=Depends(authenticate),
):
    """
    Busca medicamentos por nombre
    """
    _, _ = authentication
    # TODO: @ignacio.pieve This method should be moved to this folder
    return Medicine.search(medicine_name)
