import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_, exc

from config import translations
from dependencies import auth
from models.appointments import Appointment
from schemas.appointments import AppointmentAddUpdateSchema, AppointmentSchema

router = APIRouter(prefix="/appointment", tags=["Appointment"])


@router.get(
    "/",
    response_model=List[AppointmentSchema],
    status_code=200,
    summary="Get all appointments",
)
def get_appointments(
    authentication=Depends(auth.authenticate),
):
    user, _ = authentication
    return user.appointments


@router.post(
    "/",
    response_model=List[AppointmentSchema],
    status_code=201,
    summary="Add a new appointment",
)
def add_appointment(
    appointment: AppointmentAddUpdateSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication

    appointment = appointment.dict()
    appointment["user"] = user
    appointment = Appointment(db, **appointment)
    appointment.create()

    return user.appointments


@router.post(
    "/{appointment_id}",
    response_model=List[AppointmentSchema],
    status_code=200,
    summary="Edit a measurement",
)
def update_appointment(
    appointment_id: str,
    appointment: AppointmentAddUpdateSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication

    old_appointment = Appointment(db, Appointment.id == appointment_id).get()
    if old_appointment is None:
        raise translations["errors"]["treatments"]["appointment_not_found"]

    appointment = appointment.dict()
    appointment["user"] = user
    for key, value in appointment.items():
        setattr(old_appointment, key, value)
    old_appointment.save()

    return user.appointments


@router.delete(
    "/{appointment_id}",
    response_model=List[AppointmentSchema],
    status_code=200,
    summary="Delete appointment",
)
def delete_appointment(
    appointment_id: str,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication

    # TODO: Add security
    appointment = Appointment(db, Appointment.id == appointment_id).get()
    appointment.destroy()

    return user.appointments
