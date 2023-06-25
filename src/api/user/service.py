from datetime import datetime

from sqlalchemy import delete, insert, select, update

from api.user.models import Device, User
from api.user.schemas import UserUpdateSchema
from api.user.utils import generate_code
from database import database


async def get_or_create_user(user_id: str, email: str) -> User:
    """
    Retrieves a user from the database based on the given user ID.
    If the user does not exist, a new user is created with the provided ID and email.

    Args:
        user_id (str): The ID of the user to retrieve or create.
        email (str): The email of the user to retrieve or associate with the new user.

    Returns:
        User: The user object, either retrieved or newly created.
    """

    select_query = select(User).where(User.id == user_id)
    user = await database.fetch_one(query=select_query)

    if user is None:
        code = await generate_code()
        insert_query = (
            insert(User)
            .values(id=user_id, email=email, invitation=code)
            .returning(User)
        )
        user = await database.fetch_one(query=insert_query)

    return user


async def assert_device(user: User, device_token: str) -> bool:
    """
    Asserts that a device is associated with a user.

    Args:
        user (User): The user object to check.
        device_token (str): The device to check.

    Returns:
        bool: True if the device is associated with the user, False otherwise.
    """

    select_query = select(Device).where(
        Device.user_id == user.id, Device.token == device_token
    )
    device = await database.fetch_one(query=select_query)

    if device is None:
        insert_query = (
            insert(Device).values(user_id=user.id, token=device_token).returning(Device)
        )
        device = await database.fetch_one(query=insert_query)
    else:
        update_query = (
            update(Device)
            .where(Device.user_id == user.id, Device.token == device_token)
            .values(last_access=datetime.now())
            .returning(Device)
        )
        device = await database.fetch_one(query=update_query)

    return device


async def get_user_devices(user: User) -> list[User]:
    """
    Retrieves a user's devices from the database.

    Args:
        user (User): The user object to retrieve devices for.

    Returns:
        list[User]: The list of devices associated with the user.
    """

    select_query = select(Device).where(Device.user_id == user.id)
    devices = await database.fetch_all(query=select_query)
    return devices


def get_user(user_id: str) -> User:
    """
    Retrieves a user from the database based on the given user ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        User: The user object.
    """

    select_query = select(User).where(User.id == user_id)
    user = database.fetch_one(query=select_query)
    return user


async def update_user(user: User, new_data: UserUpdateSchema) -> User:
    """
    Updates a user with new data.

    Args:
        user (User): The user object to be updated.
        new_data (UserUpdateSchema): The updated data for the user.

    Returns:
        User: The updated user object.
    """

    update_query = (
        update(User).where(User.id == user.id).values(**new_data.dict()).returning(User)
    )
    updated_user = await database.fetch_one(query=update_query)
    return updated_user


async def delete_user(user: User):
    """
    Deletes a user from the database.

    Args:
        user (User): The user object to be deleted.
    """

    delete_query = delete(User).where(User.id == user.id)
    await database.execute(query=delete_query)
