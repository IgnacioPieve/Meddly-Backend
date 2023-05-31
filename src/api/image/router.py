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
async def get_image(name: str, user: User = Depends(authenticate)) -> Response:
    """
    Get an image.

    Parameters:
    - name (str): The name of the image.
    - user (User): The authenticated user.

    Returns:
    - Response: An HTTP response object containing the image.

    Summary:
    This function retrieves an image based on the provided name and the authenticated user.

    Responses:
    - 200: If the image is successfully retrieved, the response will contain the image content with the media type "image/jpg".
    """

    image = await get_image_service(name, user)

    return Response(content=image, media_type="image/jpg")
