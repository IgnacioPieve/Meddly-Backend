from datetime import datetime

from databases.interfaces import Record
from sqlalchemy import delete, insert, select, update

from api.measurement.models import Measurement
from api.measurement.schemas import CreateUpdateMeasurementSchema
from api.user.models import User
from database import database


async def get_measurements(user: User, start: datetime, end: datetime) -> list[Record]:
    """
    Get measurements.

    Retrieves measurements for the specified user within the specified time range.

    Args:
        user (User): The user object representing the user.
        start (datetime): The start datetime of the time range.
        end (datetime): The end datetime of the time range.

    Returns:
        list[Record]: A list of measurement records.
    """

    select_query = select(Measurement).where(
        Measurement.user_id == user.id,
        Measurement.date >= start,
        Measurement.date <= end,
    )
    return await database.fetch_all(query=select_query)


async def create_measurement(
    user: User, measurement: CreateUpdateMeasurementSchema
) -> Record | None:
    """
    Create a measurement.

    Creates a new measurement for the specified user.

    Args:
        user (User): The user object representing the user.
        measurement (CreateUpdateMeasurementSchema): The measurement data to be created.

    Returns:
        Record | None: The created measurement record or None if creation failed.
    """

    insert_query = (
        insert(Measurement)
        .values(user_id=user.id, **measurement.dict())
        .returning(Measurement)
    )
    measurement = await database.fetch_one(query=insert_query)
    return measurement


async def update_measurement(
    user: User, measurement_id: int, measurement: CreateUpdateMeasurementSchema
) -> Record | None:
    """
    Update a measurement.

    Updates an existing measurement for the specified user.

    Args:
        user (User): The user object representing the user.
        measurement_id (int): The ID of the measurement to be updated.
        measurement (CreateUpdateMeasurementSchema): The updated measurement data.

    Returns:
        Record | None: The updated measurement record or None if update failed.
    """

    update_query = (
        update(Measurement)
        .where(
            Measurement.id == measurement_id,
            Measurement.user_id == user.id,
        )
        .values(**measurement.dict())
        .returning(Measurement)
    )
    measurement = await database.fetch_one(query=update_query)
    return measurement


async def delete_measurement(user: User, measurement_id: int) -> bool:
    """
    Delete a measurement.

    Deletes an existing measurement for the specified user.

    Args:
        user (User): The user object representing the user.
        measurement_id (int): The ID of the measurement to be deleted.

    Returns:
        bool: True if deletion was successful, False otherwise.
    """

    delete_query = (
        delete(Measurement)
        .where(
            Measurement.id == measurement_id,
            Measurement.user_id == user.id,
        )
        .returning(Measurement)
    )
    deleted = bool(await database.execute(query=delete_query))
    return deleted
