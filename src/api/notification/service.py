from sqlalchemy import delete, insert, select

from api.notification.exceptions import ERROR500, ERROR501
from api.notification.models.notification import NotificationPreference
from api.user.models import User
from database import database


async def get_notification_preferences(user: User) -> list[str]:
    """
    Get notification preferences.

    Args:
        user (User): The authenticated user.

    Returns:
        list[str]: A list of notification preferences.

    Summary:
    This function retrieves the notification preferences for the authenticated user. It queries the database to fetch all notification preferences associated with the user and returns them as a list of strings.

    """

    select_query = select(NotificationPreference).where(
        NotificationPreference.user_id == user.id
    )
    results = await database.fetch_all(query=select_query)
    return [result.notification_preference for result in results]


async def add_notification_preference(
    notification_preference: str, user: User
) -> list[str]:
    """
    Add a notification preference.

    Args:
        notification_preference (str): The notification preference to add.
        user (User): The authenticated user.

    Returns:
        list[str]: A list of updated notification preferences.

    Raises:
        ERROR500: If the addition of the notification preference fails.

    Summary:
    This function adds a notification preference for the authenticated user. It inserts a new record in the database with the provided notification preference and the user's ID. If the insertion is successful, it retrieves the updated list of notification preferences and returns it. If the insertion fails, it raises an ERROR500.

    """

    select_query = select(NotificationPreference).where(
        NotificationPreference.user_id == user.id,
        NotificationPreference.notification_preference == notification_preference,
    )
    result = await database.fetch_one(query=select_query)
    if result:
        raise ERROR500

    insert_query = (
        insert(NotificationPreference)
        .values(user_id=user.id, notification_preference=notification_preference)
        .returning(NotificationPreference)
    )
    await database.execute(query=insert_query)
    preferences = await get_notification_preferences(user)
    return preferences


async def delete_notification_preference(
    notification_preference: str, user: User
) -> list[str]:
    """
    Delete a notification preference.

    Args:
        notification_preference (str): The notification preference to delete.
        user (User): The authenticated user.

    Returns:
        list[str]: A list of updated notification preferences.

    Raises:
        ERROR501: If the deletion of the notification preference fails.

    Summary:
    This function deletes a notification preference for the authenticated user. It removes the corresponding record from the database based on the provided notification preference and the user's ID. If the deletion is successful, it retrieves the updated list of notification preferences and returns it. If the deletion fails, it raises an ERROR501.

    """

    select_query = select(NotificationPreference).where(
        NotificationPreference.user_id == user.id,
        NotificationPreference.notification_preference == notification_preference,
    )
    result = await database.fetch_one(query=select_query)
    if not result:
        raise ERROR501

    delete_query = (
        delete(NotificationPreference)
        .where(
            NotificationPreference.user_id == user.id,
            NotificationPreference.notification_preference == notification_preference,
        )
        .returning(NotificationPreference)
    )
    await database.execute(query=delete_query)
    preferences = await get_notification_preferences(user)
    return preferences
