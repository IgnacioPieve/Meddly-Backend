from user_calendar.models.medicine import Consumption, Medicine
from user_calendar.schemas.medicine import (
    AddConsumptionSchema,
    DeleteConsumptionSchema,
    MedicineAddSchema,
    MedicineSchema,
    MedicineUpdateSchema,
)

from fastapi import APIRouter, Depends

from auth.dependencies import authenticate
from models import raise_errorcode

router = APIRouter(prefix="/medicines")


@router.get(
    "", status_code=200, response_model=list[MedicineSchema], include_in_schema=False
)
@router.get(
    "/",
    status_code=200,
    response_model=list[MedicineSchema],
    summary="Get all active medicines",
)
def get_medicines(authentication=Depends(authenticate)):
    user, _ = authentication
    active_medicines, _ = user.get_active_medicines_with_consumptions()
    return active_medicines


@router.post("/medicine", status_code=201, include_in_schema=False)
@router.post("/medicine/", status_code=201, summary="Add a new medicine")
def add_medicine(medicine: MedicineAddSchema, authentication=Depends(authenticate)):
    """
    Añande una preferencia de notificación
    """
    user, db = authentication

    medicine = medicine.dict()
    medicine["start_date"] = medicine["start_date"].date()
    medicine["end_date"] = (
        medicine["end_date"].date() if medicine.get("end_date") else None
    )
    medicine = Medicine(db, user=user, **medicine)
    medicine.create()


@router.post("/medicine/{medicine_id}", status_code=200, include_in_schema=False)
@router.post("/medicine/{medicine_id}/", status_code=200, summary="Modify a medicine")
def modify_medicine(
    medicine_id: int,
    medicine: MedicineUpdateSchema,
    authentication=Depends(authenticate),
):
    user, db = authentication
    medicine_data = medicine.dict()
    medicine_data["start_date"] = medicine_data["start_date"].date()
    medicine_data["end_date"] = (
        medicine_data["end_date"].date() if medicine_data.get("end_date") else None
    )

    medicine = Medicine(db, Medicine.id == medicine_id).get()
    if medicine is None:
        raise_errorcode(305)
    if medicine.user != user:
        raise_errorcode(306)
    for key, value in medicine_data.items():
        setattr(medicine, key, value)
    medicine.save()


@router.delete("/medicine/{medicine_id}", status_code=200, include_in_schema=False)
@router.delete("/medicine/{medicine_id}/", status_code=200, summary="Delete a medicine")
def delete_medicine(medicine_id: int, authentication=Depends(authenticate)):
    user, db = authentication
    medicine = Medicine(db, Medicine.id == medicine_id).get()
    if medicine is None:
        raise_errorcode(305)
    if medicine.user != user:
        raise_errorcode(306)
    medicine.destroy()


@router.post("/consumption", status_code=201, include_in_schema=False)
@router.post(
    "/consumption/",
    status_code=201,
    summary="Add a new consumption",
)
def add_consumption(
    consumption: AddConsumptionSchema, authentication=Depends(authenticate)
):
    user, db = authentication
    medicine = Medicine(db, Medicine.id == consumption.medicine_id).get()
    if medicine is None:
        raise_errorcode(305)

    consumption = consumption.dict()
    consumption = Consumption(db, medicine=medicine, **consumption)
    consumption.create()


@router.post("/consumption_delete", status_code=200, include_in_schema=False)
@router.post("/consumption_delete/", status_code=200, summary="Delete a consumption")
def delete_consumption(
    consumption: DeleteConsumptionSchema, authentication=Depends(authenticate)
):
    user, db = authentication
    consumption = Consumption(
        db,
        Consumption.medicine_id == consumption.medicine_id,
        Consumption.date == consumption.date,
    ).get()
    if consumption is None:
        raise_errorcode(305)
    if consumption.medicine.user != user:
        raise_errorcode(306)
    consumption.destroy()
