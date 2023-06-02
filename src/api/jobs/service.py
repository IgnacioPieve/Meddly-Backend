from datetime import datetime

from fastapi import BackgroundTasks
from sqlalchemy import select

from api.appointment.models import Appointment
from api.appointment.service import get_appointments
from api.notification.models.message import TodayUserAppointments
from api.notification.service import send_notification
from api.user.models import User
from database import database


async def send_today_user_appointments_notification(background_tasks: BackgroundTasks):
    select_query = select(User).where(
        Appointment.user_id == User.id,
        Appointment.date
        >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
        Appointment.date
        <= datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
    )
    users = await database.fetch_all(query=select_query)
    for user in users:
        user = User(**user)
        appointments = await get_appointments(
            user,
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
        )
        message = TodayUserAppointments(user=user, appointments=appointments)
        await send_notification(message, user, background_tasks)


# async def send_today_user_medicines_notification(background_tasks: BackgroundTasks):
#     select_query = (
#         select(User)
#         .where(
#             Appointment.user_id == User.id,
#             Appointment.date >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
#             Appointment.date <= datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
#         )
#     )
#     users = await database.fetch_all(query=select_query)
