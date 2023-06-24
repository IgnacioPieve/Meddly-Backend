from typing import Annotated, Literal

from fastapi import APIRouter, Depends, Query

from api.auth.dependencies import authenticate
from api.exceptions import GenericException
from api.notification.schemas import NotificationSchema
from api.notification.service import (
    add_notification_preference as add_notification_preference_service,
)
from api.notification.service import delete_notification as delete_notification_service
from api.notification.service import (
    delete_notification_preference as delete_notification_preference_service,
)
from api.notification.service import (
    get_notification_preferences as get_notification_preferences_service,
)
from api.notification.service import get_notifications as get_notifications_service
from api.user.models import User

router = APIRouter(prefix="/notification", tags=["Notifications"])


@router.get(
    "/preference",
    response_model=list[str],
    status_code=200,
    summary="Get notification preferences",
)
async def get_notification_preferences(user: User = Depends(authenticate)):
    """
    # Get notification preferences

    This endpoint retrieves the notification preferences for the authenticated user.

    Args:
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **list[str]**: A list of notification preferences.
    """

    results = await get_notification_preferences_service(user)
    return results


@router.post(
    "/preference",
    response_model=list[str],
    status_code=201,
    summary="Add a notification preference",
)
async def add_notification_preference(
    notification_preference: Literal["email", "whatsapp", "push"],
    user: User = Depends(authenticate),
):
    """
    # Add a notification preference

    This endpoint adds a notification preference for the authenticated user.

    Args:
    - **notification_preference** (Literal["email", "whatsapp", "push"]): The notification preference to add.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **list[str]**: A list of updated notification preferences.
    """
    try:
        result = await add_notification_preference_service(notification_preference, user)
    except GenericException as e:
        raise e.http_exception
    return result


@router.delete(
    "/preference",
    response_model=list[str],
    status_code=200,
    summary="Delete a notification preference",
)
async def delete_notification_preference(
    notification_preference: Literal["email", "whatsapp", "push"],
    user: User = Depends(authenticate),
):
    """
    # Delete a notification preference

    This endpoint deletes a notification preference for the authenticated user.

    Args:
    - **notification_preference** (Literal["email", "whatsapp", "push"]): The notification preference to delete.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **list[str]**: A list of updated notification preferences.
    """

    try:
        result = await delete_notification_preference_service(notification_preference, user)
    except GenericException as e:
        raise e.http_exception
    return result


@router.get(
    "",
    response_model=list[NotificationSchema],
    status_code=200,
    summary="Get notifications",
)
async def get_notifications(
    type: Annotated[list[str] | None, Query()] = None,
    page: int = 1,
    per_page: int = 10,
    user: User = Depends(authenticate),
):
    """
    # Get notifications

    This endpoint retrieves the notifications for the authenticated user.

    Args:
    - **type** (list[str] | None): The notification types to retrieve. If not specified, all notification types will be retrieved.
    - **page** (int): The page number to retrieve. Defaults to 1.
    - **per_page** (int): The number of notifications to retrieve per page. Defaults to 10.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **list[NotificationSchema]**: A list of notifications.
    """

    results = await get_notifications_service(
        user, page=page, per_page=per_page, type=type
    )
    return results


@router.delete(
    "",
    status_code=200,
    summary="Delete a notification",
)
async def delete_notification(
    notification_id: int,
    user: User = Depends(authenticate),
):
    """
    # Delete a notification

    This endpoint deletes a notification for the authenticated user.

    Args:
    - **notification_id** (int): The ID of the notification to delete.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.
    """
    try:
        await delete_notification_service(notification_id=notification_id, user=user)
    except GenericException as e:
        raise e.http_exception
