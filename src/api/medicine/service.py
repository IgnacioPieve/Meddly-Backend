from datetime import datetime, timedelta

from sqlalchemy import and_, delete, insert, or_, select, update
from starlette.background import BackgroundTasks

from api.medicine.exceptions import (
    ConsumptionAlreadyExists,
    ConsumptionDoesNotExist,
    MedicineNotFound,
)
from api.medicine.models import Consumption, Medicine
from api.medicine.schemas import (
    CreateConsumptionSchema,
    CreateMedicineSchema,
    DeleteConsumptionSchema,
)
from api.notification.models.message import (
    LowStockFromSupervisedUserMessage,
    LowStockMessage,
)
from api.notification.service import send_notification
from api.supervisor.service import get_supervised, get_supervisors
from api.user.models import User
from database import database


async def get_medicines(user: User) -> list[Medicine]:
    """
    Get medicines for a user within a specified time range.

    Args:
        user (User): The user for whom to retrieve medicines.
        start (datetime, optional): Start date of the time range. Defaults to None.
        end (datetime, optional): End date of the time range. Defaults to None.

    Returns:
        list[Medicine]: A list of medicines matching the criteria.

    """

    select_query = select(Medicine).where(
        Medicine.user_id == user.id,
        or_(Medicine.end_date == None, Medicine.end_date >= datetime.now()),
    )

    return await database.fetch_all(query=select_query)


async def get_medicine(user: User, medicine_id: int) -> Medicine | None:
    """
    Get a medicine for a user.

    Args:
        user (User): The user who owns the medicine.
        medicine_id (int): The ID of the medicine to retrieve.

    Returns:
        Medicine | None: The medicine, or None if not found.

    """

    select_query = select(Medicine).where(
        Medicine.id == medicine_id, Medicine.user_id == user.id
    )
    medicine = await database.fetch_one(query=select_query)
    return medicine


async def create_medicine(user: User, medicine: CreateMedicineSchema) -> Medicine:
    """
    Create a new medicine for a user.

    Args:
        user (User): The user for whom to create the medicine.
        medicine (CreateMedicineSchema): The data required to create the medicine.

    Returns:
        Medicine: The created medicine, or None if creation failed.

    """

    medicine_obj = Medicine(
        **medicine.dict(),
    )
    medicine_obj.validate()

    medicine.start_date = medicine.start_date.replace(
        hour=0, minute=0, second=0, microsecond=0
    )
    if medicine.end_date:
        medicine.end_date = medicine.end_date.replace(
            hour=0, minute=0, second=0, microsecond=0
        )

    insert_query = (
        insert(Medicine).values(user_id=user.id, **medicine.dict()).returning(Medicine)
    )
    medicine = await database.fetch_one(query=insert_query)
    return medicine


async def delete_medicine(user: User, medicine_id: int):
    """
    Delete a medicine for a user.

    Args:
        user (User): The user who owns the medicine.
        medicine_id (int): The ID of the medicine to delete.
    """

    delete_query = (
        delete(Medicine)
        .where(Medicine.id == medicine_id, Medicine.user_id == user.id)
        .returning(Medicine)
    )
    if not bool(await database.execute(query=delete_query)):
        raise MedicineNotFound


async def create_consumption(
    user: User,
    consumption: CreateConsumptionSchema,
    background_tasks: BackgroundTasks,
) -> Consumption:
    """
    Create a new consumption for a user.

    Args:
        user (User): The user for whom to create the consumption.
        consumption (CreateConsumptionSchema): The data required to create the consumption.

    Returns:
        Consumption: The created consumption.
    """

    medicine = await database.fetch_one(
        select(Medicine).where(Medicine.id == consumption.medicine_id)
    )
    if not medicine or (
        medicine.user_id != user.id
        and medicine.user_id
        not in [supervised.id for supervised in await get_supervised(user)]
    ):
        raise MedicineNotFound

    medicine = Medicine(**medicine)
    consumption_obj = Consumption(
        **consumption.dict(),
        medicine=medicine,
    )
    consumption_obj.validate()

    already_exists = bool(
        await database.fetch_one(
            select(Consumption).where(
                Consumption.date == consumption.date,
                Consumption.medicine_id == consumption.medicine_id,
            )
        )
    )
    if already_exists:
        raise ConsumptionAlreadyExists

    consumption.date = consumption.date.replace(second=0, microsecond=0)
    insert_query = (
        insert(Consumption).values(**consumption.dict()).returning(Consumption)
    )
    consumption = await database.fetch_one(query=insert_query)
    consumption.consumed = True

    if medicine.stock:
        update_query = (
            update(Medicine)
            .where(Medicine.id == consumption.medicine_id)
            .values(stock=max(medicine.stock - 1, 0))
        )
        await database.execute(query=update_query)

        if medicine.stock_warning and medicine.stock <= medicine.stock_warning:
            await send_notification(
                LowStockMessage(
                    medicine=medicine,
                ),
                user=User(**user),
                background_tasks=background_tasks,
            )
            for supervisor in await get_supervisors(user):
                await send_notification(
                    LowStockFromSupervisedUserMessage(
                        medicine=medicine,
                        supervised_user=User(**user),
                    ),
                    user=User(**supervisor),
                    background_tasks=background_tasks,
                )

    return consumption


async def delete_consumption(user: User, consumption: DeleteConsumptionSchema):
    """
    Delete a consumption for a user.

    Args:
        user (User): The user who owns the consumption.
        consumption (DeleteConsumptionSchema): The data required to delete the consumption.
    """

    medicine = await database.fetch_one(
        select(Medicine).where(Medicine.id == consumption.medicine_id)
    )
    if not medicine or (
        medicine.user_id != user.id
        and medicine.user_id
        not in [supervised.id for supervised in await get_supervised(user)]
    ):
        raise MedicineNotFound

    consumption.date = consumption.date.replace(second=0, microsecond=0)
    delete_query = (
        delete(Consumption)
        .where(
            Consumption.date == consumption.date,
            Consumption.medicine_id == consumption.medicine_id,
        )
        .returning(Consumption)
    )
    if not bool(await database.execute(query=delete_query)):
        raise ConsumptionDoesNotExist


async def get_consumptions(
    user: User, start: datetime, end: datetime
) -> list[Medicine]:
    """
    Retrieves consumptions of medicines for a specific user within a date range.

    Args:
        user (User): The user for whom to retrieve the consumptions.
        start (datetime): The start date of the range.
        end (datetime): The end date of the range.

    Returns:
        list[Medicine]: A list of consumptions.
    """

    select_query = select(Medicine).where(
        Medicine.user_id == user.id,
        and_(
            Medicine.start_date <= end,
            or_(Medicine.end_date == None, Medicine.end_date >= start),
        ),
    )
    medicines = await database.fetch_all(query=select_query)
    consumptions = {}

    for medicine in medicines:
        medicine = Medicine(**medicine)
        consumptions[medicine.id] = {}
        range_start = max(start, medicine.start_date)
        range_end = min(end, medicine.end_date or datetime.max)

        if medicine.hours:
            frequency_rule = medicine.get_frequency().between(range_start, range_end)
            for date in frequency_rule:
                consumptions[medicine.id][date.date()] = {}
                for hour in medicine.hours:
                    c_date = datetime.combine(
                        date, datetime.strptime(hour, "%H:%M").time()
                    )
                    c = Consumption(
                        date=c_date,
                        real_consumption_date=c_date,
                        medicine_id=medicine.id,
                    )
                    c.consumed = False
                    consumptions[medicine.id][date.date()][hour] = c

        consumptions_taken = await database.fetch_all(
            select(Consumption).where(
                Consumption.medicine_id == medicine.id,
                Consumption.date.between(range_start, range_end),
            )
        )
        for consumption_taken in consumptions_taken:
            consumption_taken = Consumption(**consumption_taken)
            consumption_taken.consumed = True
            if consumption_taken.date.date() not in consumptions[medicine.id]:
                consumptions[medicine.id][consumption_taken.date.date()] = {}
            consumptions[medicine.id][consumption_taken.date.date()][
                consumption_taken.date.strftime("%H:%M")
            ] = consumption_taken

    return [
        consumption
        for medicine in consumptions.values()
        for consumption in medicine.values()
        for consumption in consumption.values()
    ]


async def get_consumptions_on_date(
    user: User, date: datetime, only_not_taken: bool = False
) -> list[Consumption]:
    """
    Retrieves consumptions of medicines for a specific user on a specific date.

    Args:
        user (User): The user for whom to retrieve the consumptions.
        date (datetime): The date for which to retrieve the consumptions.

    Returns:
        list[Consumption]: A list of consumptions.
    """

    start = date.replace(hour=23, minute=59, second=59, microsecond=0) - timedelta(
        days=1
    )
    end = date.replace(hour=0, minute=0, second=1, microsecond=0) + timedelta(days=1)
    return [
        consumption
        for consumption in await get_consumptions(user, start, end)
        if consumption.date.date() == date.date()
        and (not only_not_taken or not consumption.consumed)
    ]


async def get_medicines_between_dates(
    user: User,
    start: datetime,
    end: datetime,
) -> list[Medicine]:
    """
    Retrieves medicines for a specific user within a date range.

    Args:
        user (User): The user for whom to retrieve the medicines.
        start (datetime): The start date of the range.
        end (datetime): The end date of the range.

    Returns:
        list[Medicine]: A list of medicines.
    """

    select_query = select(Medicine).where(
        Medicine.user_id == user.id,
        and_(
            Medicine.start_date <= end,
            or_(Medicine.end_date == None, Medicine.end_date >= start),
        ),
    )
    medicines = await database.fetch_all(query=select_query)
    return medicines
