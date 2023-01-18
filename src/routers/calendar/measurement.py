from fastapi import APIRouter, Depends

from dependencies import auth
from models.calendar.measurement import Measurement
from models.utils import raise_errorcode
from schemas.calendar.measurement import AddMeasurementSchema

router = APIRouter(prefix="/calendar/measurement")


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201, summary="Add a new measurement")
def add_measurement(
    measurement: AddMeasurementSchema, authentication=Depends(auth.authenticate)
):
    """
    Añande una preferencia de notificación
    """
    user, db = authentication

    measurement = measurement.dict()
    measurement = Measurement(db, user=user, **measurement)
    measurement.create()
    return


@router.post("/{measurement_id}", status_code=200, include_in_schema=False)
@router.post("/{measurement_id}/", status_code=200, summary="Modify a measurement")
def modify_measurement(
    measurement_id: int,
    measurement: AddMeasurementSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication
    measurement_data = measurement.dict()
    measurement = Measurement(db, Measurement.id == measurement_id).get()
    if measurement is None:
        raise_errorcode(600)
    if measurement.user != user:
        raise_errorcode(601)
    for key, value in measurement_data.items():
        setattr(measurement, key, value)
    measurement.save()
    return


@router.delete("/{measurement_id}", status_code=200, include_in_schema=False)
@router.delete("/{measurement_id}/", status_code=200, summary="Delete a measurement")
def delete_measurement(measurement_id: int, authentication=Depends(auth.authenticate)):
    user, db = authentication
    measurement = Measurement(db, Measurement.id == measurement_id).get()
    if measurement is None:
        raise_errorcode(600)
    if measurement.user != user:
        raise_errorcode(601)
    measurement.destroy()
    return
