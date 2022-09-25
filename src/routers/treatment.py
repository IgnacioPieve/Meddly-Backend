import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_, exc

from config import translations
from dependencies import auth
from models.treatment import (
    Consumption,
    ConsumptionRule,
    Measurement,
    Medicine,
    Treatment,
)
from schemas.treatment import (
    MeasurementAddUpdateSchema,
    MeasurementSchema,
    TreatmentAddUpdateSchema,
    TreatmentSchema,
)

router = APIRouter(prefix="/treatment", tags=["Treatment"])


@router.get(
    "/",
    response_model=List[TreatmentSchema],
    status_code=200,
    summary="List all treatments",
)
def list_treatments(authentication=Depends(auth.authenticate)):
    """
    Retorna todos los tratamientos del usuario logueado.
    """
    user, _ = authentication
    return user.treatments


@router.post(
    "/",
    response_model=List[TreatmentSchema],
    status_code=201,
    summary="Add a new treatment",
)
def add_treatment(
    treatment: TreatmentAddUpdateSchema, authentication=Depends(auth.authenticate)
):
    """
    Añande un tratamiento
    """
    user, db = authentication

    medicine = treatment.medicine.dict()
    medicine = Medicine(db, **medicine)
    medicine.create()

    consumption_rule = treatment.consumption_rule.dict()
    consumption_rule = ConsumptionRule(db, **consumption_rule)
    consumption_rule.create()

    treatment = treatment.dict()
    treatment["medicine"] = medicine
    treatment["consumption_rule"] = consumption_rule
    treatment["user"] = user
    treatment = Treatment(db, **treatment)
    treatment.create()

    return user.treatments


@router.post(
    "/{treatment_id}/",
    response_model=List[TreatmentSchema],
    status_code=200,
    summary="Update a treatment",
)
def update_treatment(
    treatment_id: int,
    treatment: TreatmentAddUpdateSchema,
    authentication=Depends(auth.authenticate),
):
    """
    Actualiza un tratamiento
    """
    user, db = authentication

    original_treatment = Treatment(db, Treatment.id == treatment_id).get()

    medicine_data = treatment.medicine.dict()
    medicine = original_treatment.medicine
    for key, value in medicine_data.items():
        setattr(medicine, key, value)
    medicine.db = db
    medicine.save()

    consumption_rule_data = treatment.consumption_rule.dict()
    consumption_rule = original_treatment.consumption_rule
    for key, value in consumption_rule_data.items():
        setattr(consumption_rule, key, value)
    consumption_rule.db = db
    consumption_rule.save()

    treatment_data = treatment.dict()
    del treatment_data["medicine"]
    del treatment_data["consumption_rule"]
    for key, value in treatment_data.items():
        setattr(original_treatment, key, value)
    original_treatment.save()

    return user.treatments


@router.delete(
    "/{treatment_id}/",
    response_model=List[TreatmentSchema],
    status_code=200,
    summary="Delete a treatment",
)
def delete_treatment(treatment_id: int, authentication=Depends(auth.authenticate)):
    """
    Elimina un tratamiento
    """
    user, db = authentication

    treatment = Treatment(db, Treatment.id == treatment_id).get()
    treatment.destroy()

    return user.treatments


@router.post(
    "/consumption/",
    response_model=List[TreatmentSchema],
    status_code=201,
    summary="Add a new consumption",
)
def add_consumption(
    treatment_id: int,
    consumption_date: datetime.datetime,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication
    treatment = Treatment(db, Treatment.id == treatment_id).get()
    if treatment is None:
        raise translations["errors"]["treatments"]["treatment_not_found"]

    consumption_rule = treatment.consumption_rule
    consumption_rule.validate_consumption(consumption_date)

    consumption = Consumption(db, treatment=treatment, datetime=consumption_date)
    try:
        consumption.create()
    except exc.IntegrityError:
        raise translations["errors"]["treatments"]["consumption_already_exists"]

    return user.treatments


@router.delete(
    "/consumption/",
    response_model=List[TreatmentSchema],
    status_code=200,
    summary="Delete consumption",
)
def add_consumption(
    treatment_id: str,
    consumption_date: datetime.datetime,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication

    consumption = Consumption(
        db,
        and_(
            Consumption.treatment_id == treatment_id,
            Consumption.datetime.between(
                consumption_date - datetime.timedelta(seconds=5),
                consumption_date + datetime.timedelta(seconds=5),
            ),
        ),
    ).get()
    consumption.destroy()

    return user.treatments


@router.get(
    "/measurement/",
    response_model=List[MeasurementSchema],
    status_code=200,
    summary="Get measurements",
)
def get_measurements(authentication=Depends(auth.authenticate)):
    user, _ = authentication

    return user.measurements


@router.post(
    "/measurement/",
    response_model=List[MeasurementSchema],
    status_code=201,
    summary="Add a new measurement",
)
def add_measurement(
    measurement: MeasurementAddUpdateSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication
    measurement = measurement.dict()
    measurement["user"] = user
    measurement = Measurement(db, **measurement)
    measurement.create()

    return user.measurements


@router.post(
    "/measurement/{measurement_id}/",
    response_model=List[MeasurementSchema],
    status_code=200,
    summary="Edit a measurement",
)
def update_measurement(
    measurement_id: str,
    measurement: MeasurementAddUpdateSchema,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication

    old_measurement = Measurement(db, Measurement.id == measurement_id).get()
    if old_measurement is None:
        raise translations["errors"]["treatments"]["measurement_not_found"]

    measurement = measurement.dict()
    measurement["user"] = user
    for key, value in measurement.items():
        setattr(old_measurement, key, value)
    old_measurement.save()

    return user.measurements


@router.delete(
    "/measurement/{measurement_id}/",
    response_model=List[MeasurementSchema],
    status_code=200,
    summary="Delete measurement",
)
def delete_measurement(
    measurement_id: str,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication

    # TODO: Add security
    measurement = Measurement(db, Measurement.id == measurement_id).get()
    measurement.destroy()

    return user.measurements
