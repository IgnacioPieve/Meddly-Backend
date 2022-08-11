from fastapi import APIRouter, Depends
from sqlalchemy import and_, exc

from config import translations
from dependencies import auth
from models.notification import NotificationPreference
from schemas.user import UserSchema

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# @router.delete(
#     "/supervisor/{supervisor_id}", response_model=UserSchema, status_code=200, summary="Delete supervisor"
# )
# async def delete_supervisor(
#     supervisor_id: str,
#     authentication=Depends(auth.authenticate)
# ):
#     """
#     Elimina un supervisor
#     """
#     user, db = authentication
#     supervisor = Supervised(db, and_(Supervised.supervisor_id == supervisor_id, Supervised.supervised == user)).get()
#     if supervisor is None:
#         raise translations['errors']['supervisors']['supervisor_not_found']
#     supervisor.destroy()
#     return user
#
#
# @router.delete(
#     "/supervised/{supervised_id}", response_model=UserSchema, status_code=200, summary="Delete supervised"
# )
# async def delete_supervised(
#     supervised_id: str,
#     authentication=Depends(auth.authenticate)
# ):
#     """
#     Elimina un supervisado
#     """
#     user, db = authentication
#     supervised = Supervised(db, and_(Supervised.supervisor == user, Supervised.supervised_id == supervised_id)).get()
#     if supervised is None:
#         raise translations['errors']['supervisors']['supervised_not_found']
#     supervised.destroy()
#     return user


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
