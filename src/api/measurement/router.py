from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate
from api.measurement.exceptions import ERROR600
from api.measurement.schemas import CreateUpdateMeasurementSchema, MeasurementSchema
from api.measurement.service import create_measurement as create_measurement_service
from api.measurement.service import delete_measurement as delete_measurement_service
from api.measurement.service import get_measurements as get_measurements_service
from api.measurement.service import update_measurement as update_measurement_service
from api.user.models import User

router = APIRouter(prefix="/measurement", tags=["Measurement"])


@router.get(
    "",
    status_code=200,
    response_model=list[MeasurementSchema],
    summary="Get all measurements",
)
async def get_measurements(
    start: datetime | None = None,
    end: datetime | None = None,
    user: User = Depends(authenticate),
):
    """
    Get all measurements.

    Retrieves all measurements for the specified user within the specified time range.

    Args:
        start (datetime, optional): The start datetime of the time range. Defaults to 15 days ago if not provided.
        end (datetime, optional): The end datetime of the time range. Defaults to 15 days from now if not provided.
        user (User): The authenticated user. This parameter is automatically obtained from the request.


    Returns:
        List[MeasurementSchema]: List of MeasurementSchema objects representing the measurements within the specified time range.
    """

    if not start:
        start = datetime.now() - timedelta(days=15)
    if not end:
        end = datetime.now() + timedelta(days=15)

    measurements = await get_measurements_service(user, start=start, end=end)
    return measurements


@router.post("", status_code=201, summary="Create a new measurement")
async def create_measurement(
    measurement: CreateUpdateMeasurementSchema, user: User = Depends(authenticate)
):
    """
    Create a new measurement.

    This endpoint allows the authenticated user to create a new measurement.

    Args:
        measurement (CreateUpdateMeasurementSchema): The measurement data to be created.
        user (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
        The newly created measurement data.
    """

    measurement = await create_measurement_service(user, measurement)
    return measurement


@router.post("/{measurement_id}", status_code=200, summary="Update a measurement")
async def update_measurement(
    measurement_id: int,
    measurement: CreateUpdateMeasurementSchema,
    user: User = Depends(authenticate),
):
    """
    Update a measurement.

    This endpoint allows the authenticated user to update an existing measurement.

    Args:
    - measurement_id (int): The ID of the measurement to be updated.
    - measurement (CreateUpdateMeasurementSchema): The updated measurement data.
    - user (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - The updated measurement data.

    Raises:
    - HTTPException (status.HTTP_400_BAD_REQUEST): If the measurement is not found
        or the user does not have permission to access it.
    """

    measurement = await update_measurement_service(user, measurement_id, measurement)
    if measurement is None:
        raise ERROR600
    return measurement


@router.delete("/{measurement_id}", status_code=200, summary="Delete a measurement")
async def delete_measurement(measurement_id: int, user: User = Depends(authenticate)):
    """
    Delete a measurement.

    This endpoint allows the authenticated user to delete an existing measurement.

    Args:
    - measurement_id (int): The ID of the measurement to be deleted.
    - user (User): Authentication dependency. This parameter is automatically obtained from the request.

    Returns:
    - None

    Raises:
    - HTTPException (status.HTTP_400_BAD_REQUEST): If the measurement cannot be deleted.
    """

    success = await delete_measurement_service(user, measurement_id)
    if not success:
        raise ERROR600
