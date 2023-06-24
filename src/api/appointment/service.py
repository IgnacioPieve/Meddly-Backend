from datetime import datetime

from sqlalchemy import delete, insert, select, update

from api.appointment.exceptions import AppointmentDoesNotExist
from api.appointment.models import Appointment
from api.appointment.schemas import CreateUpdateAppointmentSchema
from api.user.models import User
from database import database


async def get_appointments(
    user: User, start: datetime, end: datetime
) -> list[Appointment]:
    """
    Get appointments.

    Retrieves appointments for the specified user within the specified time range.

    Args:
        user (User): The user object representing the user.
        start (datetime): The start datetime of the time range.
        end (datetime): The end datetime of the time range.

    Returns:
        list[Appointment]: The list of appointments for the specified user within the specified time range.
    """

    select_query = select(Appointment).where(
        Appointment.user_id == user.id,
        Appointment.date >= start,
        Appointment.date <= end,
    )
    return await database.fetch_all(query=select_query)


async def create_appointment(
    user: User, appointment: CreateUpdateAppointmentSchema
) -> Appointment | None:
    """
    Create appointment.

    Creates a new appointment for the specified user.

    Args:
        user (User): The user object representing the user.
        appointment (CreateUpdateAppointmentSchema): The appointment data to be created.

    Returns:
        Union[Appointment, None]: The created appointment or None if creation failed.
    """

    insert_query = (
        insert(Appointment)
        .values(user_id=user.id, **appointment.dict())
        .returning(Appointment)
    )
    appointment = await database.fetch_one(query=insert_query)
    return appointment


async def update_appointment(
    user: User, appointment_id: int, appointment: CreateUpdateAppointmentSchema
) -> Appointment | None:
    """
    Update appointment.

    Updates an existing appointment for the specified user.

    Args:
        user (User): The user object representing the user.
        appointment_id (int): The ID of the appointment to be updated.
        appointment (CreateUpdateAppointmentSchema): The updated appointment data.

    Returns:
        Union[Appointment, None]: The updated appointment or None if update failed.
    """

    update_query = (
        update(Appointment)
        .where(Appointment.id == appointment_id, Appointment.user_id == user.id)
        .values(**appointment.dict())
        .returning(Appointment)
    )
    appointment = await database.fetch_one(query=update_query)
    return appointment


async def delete_appointment(appointment_id: int, user: User):
    """
    Delete appointment.

    Deletes an existing appointment for the specified user.

    Args:
        appointment_id (int): The ID of the appointment to be deleted.
        user (User): The user object representing the user.
    """

    delete_query = (
        delete(Appointment)
        .where(Appointment.id == appointment_id, Appointment.user_id == user.id)
        .returning(Appointment)
    )
    if not bool(await database.execute(query=delete_query)):
        raise AppointmentDoesNotExist
