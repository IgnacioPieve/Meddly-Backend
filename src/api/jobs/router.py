from fastapi import APIRouter, BackgroundTasks

from api.jobs.service import (
    send_today_user_appointments_notification as send_today_user_appointments_notification_service,
)

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "/send_today_user_appointments_notification",
    status_code=200,
    summary="Send today user appointments notification",
)
async def send_today_user_appointments_notification(background_tasks: BackgroundTasks):
    await send_today_user_appointments_notification_service(background_tasks)
