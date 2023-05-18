from fastapi import APIRouter, Depends

from dependencies import auth
from models.calendar.appointment import Appointment
from models.utils import raise_errorcode
from schemas.calendar.appointment import AddAppointmentSchema, AppointmentSchema

router = APIRouter(prefix="/calendar/appointment")


@router.get("", status_code=200, response_model=list[AppointmentSchema], include_in_schema=False)
@router.get("/", status_code=200, response_model=list[AppointmentSchema], summary="Get all appointments")
def get_appointments(authentication=Depends(auth.authenticate)):
    user, _ = authentication
    return user.get_appointments()


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201, summary="Add a new appointment")
def add_appointment(
    appointment: AddAppointmentSchema, authentication=Depends(auth.authenticate)
):
    user, db = authentication
    appointment = appointment.dict()
    appointment = Appointment(db, user=user, **appointment)
    appointment.create()
    return


@router.post("/{appointment_id}", status_code=200, include_in_schema=False)
@router.post("/{appointment_id}/", status_code=200, summary="Modify an appointment")
def modify_appointment(
    appointment_id: int,
    appointment: AddAppointmentSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication
    appointment_data = appointment.dict()
    appointment = Appointment(db, Appointment.id == appointment_id).get()
    if appointment is None:
        raise_errorcode(400)
    if appointment.user != user:
        raise_errorcode(401)
    for key, value in appointment_data.items():
        setattr(appointment, key, value)
    appointment.save()
    return


@router.delete("/{appointment_id}", status_code=200, include_in_schema=False)
@router.delete("/{appointment_id}/", status_code=200, summary="Delete an appointment")
def delete_appointment(appointment_id: int, authentication=Depends(auth.authenticate)):
    user, db = authentication
    appointment = Appointment(db, Appointment.id == appointment_id).get()
    if appointment is None:
        raise_errorcode(400)
    if appointment.user != user:
        raise_errorcode(401)
    appointment.destroy()
    return
