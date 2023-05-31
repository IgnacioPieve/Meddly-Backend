from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate
from api.user.models import User
from api.user.schemas import UserSchema, UserUpdateSchema
from api.user.service import delete_user as delete_user_service
from api.user.service import update_user as update_user_service

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=UserSchema, status_code=200, summary="Get user data")
async def get_user(user: User = Depends(authenticate)) -> User:
    """
    Retrieve user data.

    This endpoint returns the data of the authenticated user.

    Returns:
        User: The user data.
    """
    return user


@router.post("", response_model=UserSchema, status_code=200, summary="Update user data")
async def update_user(
    update_data: UserUpdateSchema, user: User = Depends(authenticate)
):
    """
    Update user data.

    This endpoint updates the data of the authenticated user with the provided update data.

    Args:
        update_data (UserUpdateSchema): The data to update the user with.

    Returns:
        User: The updated user data.
    """
    updated_user = await update_user_service(user, update_data)
    return updated_user


@router.delete("", status_code=200, summary="Delete user")
async def delete_user(user: User = Depends(authenticate)):
    """
    Delete user.

    This endpoint deletes the authenticated user from the system.
    """
    await delete_user_service(user)
