import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import and_, exc

from config import translations
from dependencies import auth
from models.treatment import (
    Consumption,
    ConsumptionRule,
    Medicine,
    Treatment
)
from schemas.treatment import TreatmentAddUpdateSchema, TreatmentSchema

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
    Añande una preferencia de notificación
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
    "/consumption",
    response_model=List[TreatmentSchema],
    status_code=201,
    summary="Add a new consumption",
)
def add_consumption(
    treatment_id: str,
    consumption_date: datetime.datetime,
    authentication=Depends(auth.authenticate),
):
    user, db = authentication
    treatment = Treatment(db, Treatment.id == treatment_id).get()
    if treatment is None:
        raise translations["errors"]["treatments"]["treatment_not_found"]

    consumption_rule = treatment.treatment_indication.consumption_rule
    consumption_rule.validate_consumption(consumption_date)

    consumption = Consumption(db, treatment=treatment, datetime=consumption_date)
    try:
        consumption.create()
    except exc.IntegrityError:
        raise translations["errors"]["treatments"]["consumption_already_exists"]

    return user.treatments


@router.delete(
    "/consumption",
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
