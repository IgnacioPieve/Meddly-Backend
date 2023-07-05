from typing import List

from fastapi import BackgroundTasks
from firebase_admin import messaging
from sendgrid import Mail, SendGridAPIClient
from sqlalchemy import delete, insert, select, update

from api.notification.exceptions import (
    ThisNotificationDoesNotExist,
    YouAlreadyHaveThisNotificationPreference,
    YouDontHaveThisNotificationPreference,
)
from api.notification.models.message import Message
from api.notification.models.notification import Notification
from api.notification.models.notification_preference import NotificationPreference
from api.user.models import Device, User
from api.user.service import get_user_devices
from config import SENDGRID_CONFIG, TWILIO_NUMBER, WhatsappClient
from database import database


async def get_notification_preferences(user: User) -> list[str]:
    """
    Get notification preferences.

    This function retrieves the notification preferences for the authenticated user. It queries the database to fetch all notification preferences associated with the user and returns them as a list of strings.


    Args:
        user (User): The authenticated user.

    Returns:
        list[str]: A list of notification preferences.
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

    This function adds a notification preference for the authenticated user. It inserts a new record in the database with the provided notification preference and the user's ID. If the insertion is successful, it retrieves the updated list of notification preferences and returns it. If the insertion fails, it raises an ERROR500.


    Args:
        notification_preference (str): The notification preference to add.
        user (User): The authenticated user.

    Returns:
        list[str]: A list of updated notification preferences. I.e. ["email", "whatsapp", "push"]
    """

    select_query = select(NotificationPreference).where(
        NotificationPreference.user_id == user.id,
        NotificationPreference.notification_preference == notification_preference,
    )
    result = await database.fetch_one(query=select_query)
    if result:
        raise YouAlreadyHaveThisNotificationPreference

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

    This function deletes a notification preference for the authenticated user. It removes the corresponding record from the database based on the provided notification preference and the user's ID. If the deletion is successful, it retrieves the updated list of notification preferences and returns it. If the deletion fails, it raises an ERROR501.

    Args:
        notification_preference (str): The notification preference to delete.
        user (User): The authenticated user.

    Returns:
        list[str]: A list of updated notification preferences.
    """

    select_query = select(NotificationPreference).where(
        NotificationPreference.user_id == user.id,
        NotificationPreference.notification_preference == notification_preference,
    )
    result = await database.fetch_one(query=select_query)
    if not result:
        raise YouDontHaveThisNotificationPreference

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


async def send_notification(
    message: Message, user: User, background_tasks: BackgroundTasks
):
    """
    Send a notification.

    This function sends a notification to the authenticated user.
    It inserts a new record in the database with the provided notification data and the user's ID.
    It also sends the notification to the user's notification preferences (email, WhatsApp, push notification).

    Args:
        message (Message): The message to send.
        user (User): The authenticated user.
        background_tasks (BackgroundTasks): The background tasks object.
    """

    def send_email(message: Message, user: User):
        message_constructor = Mail(
            from_email=SENDGRID_CONFIG["email"],
            to_emails=user.email,
        )
        message_constructor.template_id = "d-5e634cd5cd6548b4b440f188c1d2a40a"
        message_data = message.email()
        message_constructor.dynamic_template_data = {
            "hi_message": f"Hola {user.get_fullname()}!",
            "message": message_data["message"],
            "subject": message_data["subject"],
        }
        client = SendGridAPIClient(SENDGRID_CONFIG["api_key"])
        client.send(message_constructor)

    def send_whatsapp(message: Message, user: User):
        WhatsappClient.messages.create(
            from_=f"whatsapp:{TWILIO_NUMBER}",
            body=message.whatsapp()["message"],
            to=f"whatsapp:{user.phone}",
        )

    async def send_push(message: Message, user: User):
        devices = await get_user_devices(user)
        message_data = message.push()

        for device in devices:
            device: Device
            message_constructor = messaging.Message(
                notification=messaging.Notification(
                    title=message_data["title"],
                    body=message_data["body"],
                ),
                token=device.token,
            )
            messaging.send(message_constructor)

    notification_preferences = await get_notification_preferences(user)

    message_data = message.push()
    insert_query = insert(Notification).values(
        user_id=user.id,
        title=message_data["title"],
        body=message_data["body"],
        type=message.type,
    )
    await database.execute(query=insert_query)

    for notification_preference in notification_preferences:
        if notification_preference == "email":
            background_tasks.add_task(send_email, message, user)
        if notification_preference == "whatsapp":
            background_tasks.add_task(send_whatsapp, message, user)
        if notification_preference == "push":
            background_tasks.add_task(send_push, message, user)


async def get_notifications(
    user: User,
    page: int,
    per_page: int,
    type: List[str] = None,
) -> list[Notification]:
    """
    Get notifications.

    This function retrieves a list of notifications for the authenticated user.
    It retrieves the notifications from the database based on the provided page and per_page parameters.
    It also updates the is_read field of the retrieved notifications to True.

    Args:
        user (User): The authenticated user.
        page (int): The page number.
        per_page (int): The number of notifications per page.
        type (List[str], optional): The notification types to retrieve. Defaults to None.

    Returns:
        list[Notification]: A list of notifications.
    """

    select_query = (
        select(Notification)
        .where(Notification.user_id == user.id)
        .order_by(Notification.created_at.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    if type:
        select_query = select_query.where(Notification.type.in_(type))
    notifications = await database.fetch_all(query=select_query)
    update_query = (
        update(Notification)
        .where(Notification.id.in_([notification.id for notification in notifications]))
        .values(is_read=True)
    )
    await database.execute(query=update_query)
    return notifications


async def delete_notification(notification_id: int, user: User):
    """
    Delete a notification.

    This function deletes a notification for the authenticated user.

    Args:
        notification_id (int): The notification ID.
        user (User): The authenticated user.
    """

    delete_query = (
        delete(Notification)
        .where(Notification.id == notification_id, Notification.user_id == user.id)
        .returning(Notification)
    )
    result = await database.execute(query=delete_query)
    if not result:
        raise ThisNotificationDoesNotExist
    return result
