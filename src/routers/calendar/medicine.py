from fastapi import APIRouter, Depends

from dependencies import auth
from models.calendar.medicine import Consumption, Medicine
from models.utils import raise_errorcode
from schemas.calendar.medicine import (AddConsumptionSchema, MedicineAddSchema,
                                       MedicineUpdateSchema, DeleteConsumptionSchema)

router = APIRouter(prefix="/calendar/medicines")


@router.post("/medicine", status_code=201, include_in_schema=False)
@router.post("/medicine/", status_code=201, summary="Add a new medicine")
def add_medicine(
    medicine: MedicineAddSchema, authentication=Depends(auth.authenticate)
):
    """
    Añande una preferencia de notificación
    """
    user, db = authentication

    medicine = medicine.dict()
    medicine = Medicine(db, user=user, **medicine)
    medicine.create()


@router.post("/medicine/{medicine_id}", status_code=200, include_in_schema=False)
@router.post("/medicine/{medicine_id}/", status_code=200, summary="Modify a medicine")
def modify_medicine(
    medicine_id: int,
    medicine: MedicineUpdateSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication
    medicine_data = medicine.dict()
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
def delete_medicine(medicine_id: int, authentication=Depends(auth.authenticate)):
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
    consumption: AddConsumptionSchema, authentication=Depends(auth.authenticate)
):
    user, db = authentication
    medicine = Medicine(db, Medicine.id == consumption.medicine_id).get()
    if medicine is None:
        raise_errorcode(305)

    consumption = consumption.dict()
    consumption = Consumption(db, medicine=medicine, **consumption)
    consumption.create()


@router.post(
    "/consumption_delete", status_code=200, include_in_schema=False
)
@router.post(
    "/consumption_delete/", status_code=200, summary="Delete a consumption"
)
def delete_consumption(consumption: DeleteConsumptionSchema, authentication=Depends(auth.authenticate)):
    user, db = authentication
    consumption = Consumption(db,
                              Consumption.medicine_id == consumption.medicine_id,
                              Consumption.date == consumption.date).get()
    if consumption is None:
        raise_errorcode(305)
    if consumption.medicine.user != user:
        raise_errorcode(306)
    consumption.destroy()
