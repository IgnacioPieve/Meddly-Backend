from typing import Literal

from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate
from api.notification.service import (
    add_notification_preference as add_notification_preference_service,
)
from api.notification.service import (
    delete_notification_preference as delete_notification_preference_service,
)
from api.notification.service import (
    get_notification_preferences as get_notification_preferences_service,
)
from api.user.models import User

router = APIRouter(prefix="/notification", tags=["Notifications"])


@router.get(
    "",
    response_model=list[str],
    status_code=200,
    summary="Get notification preferences",
)
async def get_notification_preferences(user: User = Depends(authenticate)):
    results = await get_notification_preferences_service(user)
    return results


@router.post(
    "",
    response_model=list[str],
    status_code=201,
    summary="Add a notification preference",
)
async def add_notification_preference(
    notification_preference: Literal["email", "whatsapp", "push"],
    user: User = Depends(authenticate),
):
    result = await add_notification_preference_service(notification_preference, user)
    return result


@router.delete(
    "",
    response_model=list[str],
    status_code=200,
    summary="Delete a notification preference",
)
async def delete_notification_preference(
    notification_preference: Literal["email", "whatsapp", "push"],
    user: User = Depends(authenticate),
):
    result = await delete_notification_preference_service(notification_preference, user)
    return result
