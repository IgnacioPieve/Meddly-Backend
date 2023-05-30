from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate
from api.medicine.exceptions import ERROR305, ERROR307, GenericException
from api.medicine.schemas import (
    ConsumptionSchema,
    CreateConsumptionSchema,
    CreateMedicineSchema,
    DeleteConsumptionSchema,
    MedicineSchema,
)
from api.medicine.service import create_consumption as create_consumption_service
from api.medicine.service import create_medicine as create_medicine_service
from api.medicine.service import delete_consumption as delete_consumption_service
from api.medicine.service import delete_medicine as delete_medicine_service
from api.medicine.service import get_medicines as get_medicines_service
from api.user.models import User

router = APIRouter(prefix="/medicine", tags=["Medicine"])


@router.get(
    "/medicine",
    status_code=200,
    response_model=list[MedicineSchema],
    summary="Get all active medicines",
)
async def get_medicines(user: User = Depends(authenticate)):
    """
    Get all active medicines.

    Args:
    - user (User): User object obtained from authentication.

    Returns:
    - List[MedicineSchema]: List of MedicineSchema objects representing the active medicines.
    """

    medicines = await get_medicines_service(user)
    return medicines


@router.post(
    "/medicine",
    status_code=201,
    response_model=MedicineSchema,
    summary="Create a new medicine",
)
async def create_medicine(
    medicine: CreateMedicineSchema, user: User = Depends(authenticate)
):
    """
    Create a new medicine.

    Args:
    - medicine (CreateMedicineSchema): Data required to create a new medicine.
    - user (User): User object obtained from authentication.

    Returns:
    - MedicineSchema: The created medicine.
    """

    try:
        medicine = await create_medicine_service(user, medicine)
    except GenericException as e:
        raise e.http_exception

    return medicine


@router.delete("/medicine/{medicine_id}", status_code=200, summary="Delete a medicine")
async def delete_medicine(medicine_id: int, user: User = Depends(authenticate)):
    """
    Delete a medicine.

    Args:
    - medicine_id (int): ID of the medicine to delete.
    - user (User): User object obtained from authentication.
    """

    success = await delete_medicine_service(user, medicine_id)
    if not success:
        raise ERROR305


@router.post(
    "/consumption",
    response_model=ConsumptionSchema,
    status_code=201,
    summary="Create a new consumption",
)
async def create_consumption(
    consumption: CreateConsumptionSchema, user: User = Depends(authenticate)
):
    """
    Create a new consumption.

    Args:
    - consumption (CreateConsumptionSchema): Data required to create a new consumption.
    - user (User): User object obtained from authentication.

    Returns:
    - ConsumptionSchema: The created consumption.
    """

    try:
        consumption = await create_consumption_service(user, consumption)
    except GenericException as e:
        raise e.http_exception

    return consumption


@router.post("/consumption_delete", status_code=200, summary="Delete a consumption")
async def delete_consumption(
    consumption: DeleteConsumptionSchema, user: User = Depends(authenticate)
):
    """
    Delete a consumption.

    Args:
    - consumption (DeleteConsumptionSchema): Data required to delete a consumption.
    - user (User): User object obtained from authentication.
    """

    try:
        success = await delete_consumption_service(user, consumption)
    except GenericException as e:
        raise e.http_exception
    if not success:
        raise ERROR307
