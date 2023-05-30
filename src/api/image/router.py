from fastapi import APIRouter, Depends
from starlette.responses import Response

from api.auth.dependencies import authenticate
from api.image.service import get_image as get_image_service
from api.user.models import User

router = APIRouter(prefix="/image", tags=["Images"])


@router.get(
    "/{name}",
    responses={200: {"content": {"image/jpg": {}}}},
    response_class=Response,
    summary="Get an image",
)
async def get_image(name: str, user: User = Depends(authenticate)):
    image = await get_image_service(name, user)

    return Response(content=image, media_type="image/jpg")
