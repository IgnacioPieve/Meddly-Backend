from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from api.appointment.schemas import AppointmentSchema, CreateUpdateAppointmentSchema
from api.appointment.service import create_appointment as create_appointment_service
from api.appointment.service import delete_appointment as delete_appointment_service
from api.appointment.service import get_appointments as get_appointments_service
from api.appointment.service import update_appointment as update_appointment_service
from api.auth.dependencies import authenticate
from api.exceptions import GenericException
from api.user.models import User

router = APIRouter(prefix="/appointment", tags=["Appointment"])


@router.get(
    "",
    status_code=200,
    response_model=list[AppointmentSchema],
    summary="Get all appointments",
)
async def get_appointments(
    start: datetime | None = None,
    end: datetime | None = None,
    user: User = Depends(authenticate),
):
    """
    # Get all appointments

    This endpoint retrieves all appointments for the authenticated user within a specified time range.

    Args:
    - **start** (datetime, optional): The start datetime of the time range. Defaults to 15 days ago if not provided.
    - **end** (datetime, optional): The end datetime of the time range. Defaults to 15 days from now if not provided.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **List[AppointmentSchema]**: List of AppointmentSchema objects representing the appointments within the specified time range.
    """

    if not start:
        start = datetime.now() - timedelta(days=15)
    if not end:
        end = datetime.now() + timedelta(days=15)
    appointments = await get_appointments_service(user, start=start, end=end)
    return appointments


@router.post(
    "",
    status_code=201,
    response_model=AppointmentSchema,
    summary="Create a new appointment",
)
async def create_appointment(
    appointment: CreateUpdateAppointmentSchema, user: User = Depends(authenticate)
):
    """
    # Create a new appointment.

    This endpoint allows the authenticated user to create a new appointment.

    Args:
    - **appointment** (CreateUpdateAppointmentSchema): The appointment data to be created.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **AppointmentSchema**: The newly created appointment data.
    """

    appointment = await create_appointment_service(user, appointment)
    return appointment


@router.post(
    "/{appointment_id}",
    status_code=200,
    response_model=AppointmentSchema,
    summary="Update an appointment",
)
async def update_appointment(
    appointment_id: int,
    appointment: CreateUpdateAppointmentSchema,
    user: User = Depends(authenticate),
):
    """
    # Update an appointment.

    This endpoint allows the authenticated user to update an existing appointment.

    Args:
    - **appointment_id** (int): The ID of the appointment to be updated.
    - **appointment** (CreateUpdateAppointmentSchema): The updated appointment data.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **AppointmentSchema**: The updated appointment data.
    """

    try:
        return await update_appointment_service(user, appointment_id, appointment)
    except GenericException as e:
        raise e.http_exception


@router.delete(
    "/{appointment_id}",
    status_code=200,
    summary="Delete an appointment",
)
async def delete_appointment(appointment_id: int, user: User = Depends(authenticate)):
    """
    # Delete an appointment.

    This endpoint allows the authenticated user to delete an existing appointment.

    Args:
    - **appointment_id** (int): The ID of the appointment to be deleted.
    - **user** (User): Authentication dependency. This parameter is automatically obtained from the request.
    """

    try:
        await delete_appointment_service(appointment_id, user)
    except GenericException as e:
        raise e.http_exception
