from fastapi import APIRouter, Depends
from sqlalchemy import and_, exc

from config import translations
from dependencies import auth
from models.notification import NotificationPreference
from schemas.user import UserSchema

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.post(
    "/notification",
    response_model=UserSchema,
    status_code=201,
    summary="Add a notification preference",
)
def add_notification_preference(
    notification_preference: str, authentication=Depends(auth.authenticate)
):
    """
    Añande una preferencia de notificación
    """
    user, db = authentication
    try:
        NotificationPreference(
            db, user=user, notification_preference=notification_preference
        ).create()
    except exc.IntegrityError:
        raise translations["errors"]["notifications"][
            "notification_preference_already_exists"
        ]
    return user


@router.delete(
    "/notification",
    response_model=UserSchema,
    status_code=200,
    summary="Delete a notification preference",
)
def delete_notification_preference(
    notification_preference: str, authentication=Depends(auth.authenticate)
):
    """
    Elimina una preferencia de notificación
    """
    user, db = authentication
    notification_preference = NotificationPreference(
        db, and_(user == user, notification_preference == notification_preference)
    ).get()
    if notification_preference is None:
        raise translations["errors"]["notifications"][
            "notification_preference_not_found"
        ]
    notification_preference.destroy()
    return user
