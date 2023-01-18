from fastapi import APIRouter, Depends
from sqlalchemy import and_, exc

from config import translations
from dependencies import auth
from models.notification import NotificationPreference
from models.utils import raise_errorcode
from schemas.user import UserSchema

router = APIRouter(prefix="/notification", tags=["Notifications"])


@router.post("", response_model=UserSchema, status_code=201, include_in_schema=False)
@router.post(
    "/",
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
        raise_errorcode(501)
    return user


@router.delete("", response_model=UserSchema, status_code=200, include_in_schema=False)
@router.delete(
    "/",
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
        raise_errorcode(500)
    notification_preference.destroy()
    return user
