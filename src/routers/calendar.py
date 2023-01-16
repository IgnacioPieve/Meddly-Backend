import datetime

from fastapi import APIRouter, Depends

from dependencies import auth
from models.calendar.appointment import Appointment
from models.calendar.medicine import Consumption, Medicine
from models.user import User
from schemas.calendar import AddConsumptionSchema, CalendarSchema, MedicineAddSchema, AddAppointmentSchema

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
    user: User
    if start is None:
        start = (datetime.datetime.now() - datetime.timedelta(days=15)).date()
        end = (datetime.datetime.now() + datetime.timedelta(days=15)).date()
    return user.get_calendar(start, end)


@router.post(
    "/medicine",
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
    "/medicine/consumption",
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


@router.post(
    "/appointment",
    status_code=201,
    summary="Add a new appointment",
)
def add_appointment(
        appointment: AddAppointmentSchema,
        authentication=Depends(auth.authenticate),

):
    user, db = authentication
    appointment = appointment.dict()
    appointment = Appointment(db, user=user, **appointment)
    appointment.create()
    return
