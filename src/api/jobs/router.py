from fastapi import APIRouter, BackgroundTasks

from api.jobs.service import (
    send_today_user_appointments_notification as send_today_user_appointments_notification_service,
)
from api.jobs.service import (
    send_today_user_medicines_notification as send_today_user_medicines_notification_service,
)
from api.jobs.service import (
    send_yesterday_user_didnt_take_medicines_notification as send_yesterday_user_didnt_take_medicines_notification_service,
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "/send_today_user_appointments_notification",
    status_code=200,
    summary="Send today user appointments notification",
)
async def send_today_user_appointments_notification(background_tasks: BackgroundTasks):
    """
    # Send today's user appointments notification

    Sends notifications to users about their appointments scheduled for today.
    """

    await send_today_user_appointments_notification_service(background_tasks)


@router.get(
    "/send_today_user_medicines_notification",
    status_code=200,
    summary="Send today user medicines notification",
)
async def send_today_user_medicines_notification(background_tasks: BackgroundTasks):
    """
    # Send today's user medicines notification

    Sends notifications to users about the medicines they need to take today.
    """

    await send_today_user_medicines_notification_service(background_tasks)


@router.get(
    "/send_yesterday_user_didnt_take_medicines_notification",
    status_code=200,
    summary="Send yesterday user didnt take medicines notification",
)
async def send_yesterday_user_didnt_take_medicines_notification(
    background_tasks: BackgroundTasks,
):
    """
    # Send yesterday's user didn't take medicines notification

    Sends notifications to users who didn't take their prescribed medicines yesterday.
    """

    await send_yesterday_user_didnt_take_medicines_notification_service(
        background_tasks
    )
