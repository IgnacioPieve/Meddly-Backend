from typing import BinaryIO
from uuid import uuid4

from PIL import Image
from sqlalchemy import insert, select

from api.image.exceptions import ERROR800
from api.image.models import Image as ImageModel
from api.user.models import User
from config import IMAGES_FOLDER
from database import database


async def get_image(name: str, user: User) -> bytes:
    """
    Get an image.

    This function retrieves an image based on the provided name and the authenticated user. It fetches the image from the database, reads its content, and returns it as bytes. If the image is not found, it raises an ERROR800.

    Args:
        name (str): The name of the image.
        user (User): The authenticated user.

    Returns:
        bytes: The content of the image as bytes.

    Raises:
        ERROR800: If the image is not found.
    """

    select_query = select(ImageModel).where(
        ImageModel.user_id == user.id,
        ImageModel.name == name,
    )
    image = await database.fetch_one(select_query)
    if image is None:
        raise ERROR800
    path = f"{IMAGES_FOLDER}/{image.name}"
    with open(path, "rb") as file:
        return file.read()


async def save_image(
    file: bytes | BinaryIO,
    user: User = None,
    size: tuple[int, int] = (512, 512),
    tag: str = "Untagged",
) -> str:
    """
    Save an image.

    Args:
        file (bytes | BinaryIO): The image to save.
        user (User, optional): The authenticated user. Defaults to None.
        size (tuple[int, int], optional): The size of the image. Defaults to (512, 512).
        tag (str, optional): The tag of the image. Defaults to "Untagged".

    Returns:
        str: The name of the image.
    """

    image = Image.open(file).resize(size)
    file_name = f"{uuid4()}.jpg"

    # Lets save the image in the store folder
    image.save(f"{IMAGES_FOLDER}/{file_name}")

    # And now we save the image in the database
    insert_query = insert(ImageModel).values(
        user_id=user.id,
        tag=tag,
        name=file_name,
    )
    await database.execute(query=insert_query)

    return file_name


async def anonymous_copy_image(name: str, tag: str = "Untagged") -> str:
    """
    Copy an image anonymously.

    Args:
        name (str): The name of the image.
        tag (str, optional): The tag of the image. Defaults to "Untagged".

    Returns:
        str: The name of the image.
    """

    image = Image.open(f"{IMAGES_FOLDER}/{name}")
    file_name = f"{uuid4()}.jpg"

    # Lets save the image in the store folder
    image.save(f"{IMAGES_FOLDER}/{file_name}")

    # And now we save the image in the database
    insert_query = insert(ImageModel).values(
        user_id=None,
        tag=tag,
        name=file_name,
    )
    await database.execute(query=insert_query)

    return file_name
