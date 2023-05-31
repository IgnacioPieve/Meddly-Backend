from sqlalchemy import delete, insert, select

from api.notification.exceptions import ERROR500, ERROR501
from api.notification.models.notification import NotificationPreference
from api.user.models import User
from database import database


async def get_notification_preferences(user: User) -> list[str]:
    select_query = select(NotificationPreference).where(
        NotificationPreference.user_id == user.id
    )
    results = await database.fetch_all(query=select_query)
    return [result.notification_preference for result in results]


async def add_notification_preference(
    notification_preference: str, user: User
) -> list[str]:
    insert_query = (
        insert(NotificationPreference)
        .values(user_id=user.id, notification_preference=notification_preference)
        .returning(NotificationPreference)
    )
    success = bool(await database.execute(query=insert_query))
    if not success:
        raise ERROR500
    preferences = await get_notification_preferences(user)
    return preferences


async def delete_notification_preference(
    notification_preference: str, user: User
) -> list[str]:
    delete_query = (
        delete(NotificationPreference)
        .where(NotificationPreference.user_id == user.id)
        .where(
            NotificationPreference.notification_preference == notification_preference
        )
        .returning(NotificationPreference)
    )
    success = bool(await database.execute(query=delete_query))
    if not success:
        raise ERROR501
    preferences = await get_notification_preferences(user)
    return preferences
