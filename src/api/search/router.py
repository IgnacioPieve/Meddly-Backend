from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate
from api.search.serializers import SearchResultSchema
from api.search.service import disease_search as disease_search_service
from api.search.service import medicine_search as medicine_search_service
from api.search.service import symptom_search as symptom_search_service
from api.user.models import User

router = APIRouter(prefix="/search", tags=["Search"])


@router.get(
    "/symptom_search",
    response_model=list[SearchResultSchema],
    status_code=200,
    summary="Symptoms Search",
)
async def symptom_search(query: str, user: User = Depends(authenticate)):
    results = await symptom_search_service(query)
    return results


@router.get(
    "/medicine_search",
    response_model=list[SearchResultSchema],
    status_code=200,
    summary="Find medicine names",
)
async def medicine_search(
    query: str,
    user: User = Depends(authenticate),
):
    results = await medicine_search_service(query)
    return results


@router.get(
    "/disease_search",
    response_model=list[SearchResultSchema],
    status_code=200,
    summary="Diseases Search",
)
async def disease_search(
    query: str,
    user: User = Depends(authenticate),
):
    results = await disease_search_service(query)
    return results
