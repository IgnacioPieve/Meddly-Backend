import datetime
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import exc

from config import translations
from dependencies import auth
from models.treatment import (
    Consumption,
    ConsumptionRule,
    Medicine,
    Method,
    Treatment,
    TreatmentIndication,
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
    response_model=TreatmentSchema,
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

    method_type = treatment.medicine.method.type
    method_class = Method.__mapper__.polymorphic_map[method_type].class_
    method = method_class(db, **treatment.medicine.method.dict())
    method.create()

    medicine = treatment.medicine.dict()
    medicine["method"] = method
    medicine = Medicine(db, **medicine)
    medicine.create()

    consumption_rule_name = treatment.treatment_indication.consumption_rule.name
    consumption_rule_class = ConsumptionRule.__mapper__.polymorphic_map[
        consumption_rule_name
    ].class_
    consumption_rule = consumption_rule_class(
        db, **treatment.treatment_indication.consumption_rule.dict()
    )
    consumption_rule.create()

    treatment_indication = treatment.treatment_indication.dict()
    treatment_indication["consumption_rule"] = consumption_rule
    treatment_indication = TreatmentIndication(db, **treatment_indication)
    treatment_indication.create()

    treatment = treatment.dict()
    treatment["medicine"] = medicine
    treatment["treatment_indication"] = treatment_indication
    treatment["user"] = user
    treatment = Treatment(db, **treatment)
    treatment.create()

    return treatment


@router.post(
    "/consumption",
    response_model=TreatmentSchema,
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

    return treatment
