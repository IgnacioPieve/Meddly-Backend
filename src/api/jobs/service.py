from datetime import datetime, timedelta

from fastapi import BackgroundTasks
from sqlalchemy import select

from api.appointment.service import get_appointments
from api.medicine.service import get_consumptions, get_medicine, get_consumptions_on_date
from api.notification.models.message import (
    TodayUserAppointments,
    TodayUserMedicines,
    YesterdarUserDidntTakeMedicine,
)
from api.notification.service import send_notification
from api.user.models import User
from database import database


async def send_today_user_appointments_notification(background_tasks: BackgroundTasks):
    select_query = select(User)
    users = await database.fetch_all(query=select_query)
    for user in users:
        user = User(**user)
        appointments = await get_appointments(
            user,
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
        )
        if appointments:
            message = TodayUserAppointments(user=user, appointments=appointments)
            await send_notification(message, user, background_tasks)


async def send_today_user_medicines_notification(background_tasks: BackgroundTasks):
    select_query = select(User)
    users = await database.fetch_all(query=select_query)
    for user in users:
        user = User(**user)
        today_consumptions = await get_consumptions_on_date(
            user=user,
            date=datetime.now(),
        )
        today_medicines = {}
        for consumption in today_consumptions:
            if consumption.medicine_id not in today_medicines:
                today_medicines[consumption.medicine_id] = {
                    "name": (await get_medicine(user, consumption.medicine_id)).name,
                    "hours": [],
                }
            today_medicines[consumption.medicine_id]["hours"].append(
                consumption.date.strftime("%H:%M")
            )
        if today_medicines:
            message = TodayUserMedicines(user=user, medicines=today_medicines)
            await send_notification(message, user, background_tasks)


async def send_yesterday_user_didnt_take_medicines_notification(
        background_tasks: BackgroundTasks,
):
    select_query = select(User)
    users = await database.fetch_all(query=select_query)
    for user in users:
        user = User(**user)
        yesterday_consumptions = await get_consumptions_on_date(
            user=user,
            date=datetime.now() - timedelta(days=1),
            only_not_taken=True
        )
        yesterday_medicines = {}
        for consumption in yesterday_consumptions:
            if consumption.medicine_id not in yesterday_medicines:
                yesterday_medicines[consumption.medicine_id] = {
                    "name": (await get_medicine(user, consumption.medicine_id)).name,
                    "hours": [],
                }
            yesterday_medicines[consumption.medicine_id]["hours"].append(
                consumption.date.strftime("%H:%M")
            )
        if yesterday_medicines:
            message = YesterdarUserDidntTakeMedicine(
                user=user, medicines=yesterday_medicines
            )
            await send_notification(message, user, background_tasks)
