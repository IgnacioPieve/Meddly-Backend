from typing import Literal

from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate
from api.notification.schemas import NotificationSchema
from api.notification.service import (
    add_notification_preference as add_notification_preference_service,
)
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
    Get notification preferences.

    Parameters:
    - user (User): The authenticated user.

    Returns:
    - list[str]: A list of notification preferences.

    Summary:
    This function retrieves the notification preferences for the authenticated user.

    Responses:
    - 200: If the notification preferences are successfully retrieved, the response will contain a list of notification preferences.

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
    Add a notification preference.

    Parameters:
    - notification_preference (Literal["email", "whatsapp", "push"]): The notification preference to add.
    - user (User): The authenticated user.

    Returns:
    - list[str]: A list of updated notification preferences.

    Summary:
    This function adds a notification preference for the authenticated user.

    Responses:
    - 201: If the notification preference is successfully added, the response will contain a list of updated notification preferences.

    """

    result = await add_notification_preference_service(notification_preference, user)
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
    Delete a notification preference.

    Parameters:
    - notification_preference (Literal["email", "whatsapp", "push"]): The notification preference to delete.
    - user (User): The authenticated user.

    Returns:
    - list[str]: A list of updated notification preferences.

    Summary:
    This function deletes a notification preference for the authenticated user.

    Responses:
    - 200: If the notification preference is successfully deleted, the response will contain a list of updated notification preferences.

    """

    result = await delete_notification_preference_service(notification_preference, user)
    return result


@router.get(
    "",
    response_model=list[NotificationSchema],
    status_code=200,
    summary="Get notifications",
)
async def get_notifications(
    page: int = 1, per_page: int = 10, user: User = Depends(authenticate)
):
    results = await get_notifications_service(user, page=page, per_page=per_page)
    return results
