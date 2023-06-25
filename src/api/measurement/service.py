from datetime import datetime

from sqlalchemy import delete, insert, select, update

from api.measurement.exceptions import MeasurementNotFound
from api.measurement.models import Measurement
from api.measurement.schemas import CreateUpdateMeasurementSchema
from api.user.models import User
from database import database


async def get_measurements(
    user: User, start: datetime, end: datetime
) -> list[Measurement]:
    """
    Get measurements.

    Retrieves measurements for the specified user within the specified time range.

    Args:
        user (User): The user object representing the user.
        start (datetime): The start datetime of the time range.
        end (datetime): The end datetime of the time range.

    Returns:
        list[Measurement]: A list of measurements.
    """

    select_query = select(Measurement).where(
        Measurement.user_id == user.id,
        Measurement.date >= start,
        Measurement.date <= end,
    )
    return await database.fetch_all(query=select_query)


async def create_measurement(
    user: User, measurement: CreateUpdateMeasurementSchema
) -> Measurement:
    """
    Create a measurement.

    Creates a new measurement for the specified user.

    Args:
        user (User): The user object representing the user.
        measurement (CreateUpdateMeasurementSchema): The measurement data to be created.

    Returns:
        Measurement: The created measurement or None if creation failed.
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
) -> Measurement:
    """
    Update a measurement.

    Updates an existing measurement for the specified user.

    Args:
        user (User): The user object representing the user.
        measurement_id (int): The ID of the measurement to be updated.
        measurement (CreateUpdateMeasurementSchema): The updated measurement data.

    Returns:
        Measurement: The updated measurement.
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

    if not measurement:
        raise MeasurementNotFound

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
    if not bool(await database.execute(query=delete_query)):
        raise MeasurementNotFound
