import datetime

from fastapi import APIRouter, Depends

from dependencies import auth
from models.calendar.medicine import Consumption, Medicine
from schemas.medicine import (AddConsumptionSchema, CalendarSchema,
                              MedicineAddSchema)

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get(
    "/",
    response_model=CalendarSchema,
    status_code=200,
    summary="Get the calendar",
)
def get_calendar(
    start: datetime.date = None,
    end: datetime.date = None,
    authentication=Depends(auth.authenticate),
):
    """
    Retorna todos los medicamentos del usuario logueado en un intervalo de tiempo.
    """
    user, _ = authentication
    if start is None:
        start = (datetime.datetime.now() - datetime.timedelta(days=15)).date()
        end = (datetime.datetime.now() + datetime.timedelta(days=15)).date()
    return user.get_calendar(start, end)


@router.post(
    "/",
    status_code=201,
    summary="Add a new medicine",
)
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


@router.post(
    "/consumption",
    status_code=201,
    summary="Add a new consumption",
)
def add_consumption(
    consumption: AddConsumptionSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication
    medicine = Medicine(db, Medicine.id == consumption.medicine_id).get()
    # if medicine is None:
    #     raise translations["errors"]["treatments"]["treatment_not_found"] # TODO: Poner un error aca

    consumption = consumption.dict()
    consumption = Consumption(db, medicine=medicine, **consumption)
    consumption.create()


#
#
# @router.delete(
#     "/consumption",
#     response_model=List[TreatmentSchema],
#     status_code=200,
#     summary="Delete consumption",
# )
# def add_consumption(
#     treatment_id: str,
#     consumption_date: datetime.datetime,
#     authentication=Depends(auth.authenticate),
# ):
#     user, db = authentication
#
#     consumption = Consumption(
#         db,
#         and_(
#             Consumption.treatment_id == treatment_id,
#             Consumption.datetime.between(
#                 consumption_date - datetime.timedelta(seconds=5),
#                 consumption_date + datetime.timedelta(seconds=5),
#             ),
#         ),
#     ).get()
#     consumption.destroy()
#
#     return user.treatments
