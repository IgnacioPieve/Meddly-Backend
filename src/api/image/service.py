from sqlalchemy import select

from api.image.exceptions import ERROR800
from api.image.models import Image as ImageModel
from api.user.models import User
from database import database


async def get_image(name: str, user: User):
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
