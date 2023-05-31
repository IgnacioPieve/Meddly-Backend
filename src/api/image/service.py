from sqlalchemy import select

from api.image.exceptions import ERROR800
from api.image.models import Image as ImageModel
from api.user.models import User
from database import database


async def get_image(name: str, user: User) -> bytes:
    """
    Get an image.

    Args:
        name (str): The name of the image.
        user (User): The authenticated user.

    Returns:
        bytes: The content of the image as bytes.

    Raises:
        ERROR800: If the image is not found.

    Summary:
    This function retrieves an image based on the provided name and the authenticated user. It fetches the image from the database, reads its content, and returns it as bytes. If the image is not found, it raises an ERROR800.

    """

    select_query = select(ImageModel).where(
        ImageModel.user_id == user.id,
        ImageModel.name == name,
    )
    image = await database.fetch_one(select_query)
    if image is None:
        raise ERROR800
    folder = "store/images"
    path = f"{folder}/{image.name}"
    with open(path, "rb") as file:
        return file.read()
