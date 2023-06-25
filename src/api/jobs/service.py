from datetime import datetime, timedelta

from fastapi import BackgroundTasks
from sqlalchemy import select

from api.appointment.service import get_appointments
from api.medicine.service import get_consumptions_on_date, get_medicine
from api.notification.models.message import (
    TodayUserAppointments,
    TodayUserMedicines,
    YesterdarUserDidntTakeMedicine,
)
from api.notification.service import send_notification
from api.supervisor.service import get_supervised
from api.user.models import User
from database import database


async def send_today_user_appointments_notification(background_tasks: BackgroundTasks):
    """
    Sends notifications to users about their appointments scheduled for today.
    """

    select_query = select(User)
    users = await database.fetch_all(query=select_query)
    for user in users:
        user = User(**user)
        appointments = await get_appointments(
            user,
            datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
            datetime.now().replace(hour=23, minute=59, second=59, microsecond=0),
        )
        supervised_users = await get_supervised(user)
        supervised_appointments = [
            {
                "name": User(**supervised_user).get_fullname(),
                "appointments": await get_appointments(
                    supervised_user,
                    datetime.now().replace(hour=0, minute=0, second=0, microsecond=0),
                    datetime.now().replace(
                        hour=23, minute=59, second=59, microsecond=0
                    ),
                ),
            }
            for supervised_user in supervised_users
        ]
        if appointments or supervised_appointments:
            message = TodayUserAppointments(
                user=user,
                appointments=appointments,
                supervised_appointments=supervised_appointments,
            )
            await send_notification(message, user, background_tasks)


async def send_today_user_medicines_notification(background_tasks: BackgroundTasks):
    """
    Sends notifications to users about the medicines they need to take today.
    """

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
        supervised_today_medicines = []
        supervised_users = await get_supervised(user)
        for supervised_user in supervised_users:
            supervised_today_consumptions = await get_consumptions_on_date(
                user=User(**supervised_user),
                date=datetime.now(),
            )
            today_medicines_supervised = {
                consumption.medicine_id: {
                    "name": (
                        await get_medicine(
                            User(**supervised_user), consumption.medicine_id
                        )
                    ).name,
                    "hours": [
                        consumption.date.strftime("%H:%M")
                        for consumption in supervised_today_consumptions
                        if consumption.medicine_id == consumption.medicine_id
                    ],
                }
                for consumption in supervised_today_consumptions
            }
            if today_medicines_supervised:
                supervised_today_medicines.append(
                    {
                        "name": User(**supervised_user).get_fullname(),
                        "medicines": today_medicines_supervised,
                    }
                )

        if today_medicines:
            message = TodayUserMedicines(
                user=user,
                medicines=today_medicines,
                supervised_medicines=supervised_today_medicines,
            )
            await send_notification(message, user, background_tasks)


async def send_yesterday_user_didnt_take_medicines_notification(
    background_tasks: BackgroundTasks,
):
    """
    Sends notifications to users about the medicines they didn't take yesterday.
    """

    select_query = select(User)
    users = await database.fetch_all(query=select_query)
    for user in users:
        user = User(**user)
        yesterday_consumptions = await get_consumptions_on_date(
            user=user, date=datetime.now() - timedelta(days=1), only_not_taken=True
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
        supervised_today_medicines = []
        supervised_users = await get_supervised(user)
        for supervised_user in supervised_users:
            supervised_today_consumptions = await get_consumptions_on_date(
                user=User(**supervised_user),
                date=datetime.now() - timedelta(days=1),
                only_not_taken=True,
            )
            today_medicines = {
                consumption.medicine_id: {
                    "name": (
                        await get_medicine(
                            User(**supervised_user), consumption.medicine_id
                        )
                    ).name,
                    "hours": [
                        consumption.date.strftime("%H:%M")
                        for consumption in supervised_today_consumptions
                        if consumption.medicine_id == consumption.medicine_id
                    ],
                }
                for consumption in supervised_today_consumptions
            }
            if today_medicines:
                supervised_today_medicines.append(
                    {
                        "name": User(**supervised_user).get_fullname(),
                        "medicines": today_medicines,
                    }
                )
        if yesterday_medicines or supervised_today_medicines:
            message = YesterdarUserDidntTakeMedicine(
                user=user,
                medicines=yesterday_medicines,
                supervised_medicines=supervised_today_medicines,
            )
            await send_notification(message, user, background_tasks)
