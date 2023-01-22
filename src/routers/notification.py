from fastapi import APIRouter, Depends
from sqlalchemy import and_, exc

from dependencies import auth
from models.notification import NotificationPreference
from models.utils import raise_errorcode

router = APIRouter(prefix="/notification", tags=["Notifications"])


@router.get("", response_model=list[str], status_code=200, include_in_schema=False)
@router.get("/", response_model=list[str], status_code=200, summary="Get notification preferences")
def get_notification_preferences(authentication=Depends(auth.authenticate)):
    """
    Obtiene las preferencias de notificación del usuario
    """
    user, _ = authentication
    return [preference.notification_preference for preference in user.notification_preferences_list]


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201, summary="Add a notification preference")
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


@router.delete("", status_code=200, include_in_schema=False)
@router.delete("/", status_code=200, summary="Delete a notification preference")
def delete_notification_preference(notification_preference: str, authentication=Depends(auth.authenticate)):
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
