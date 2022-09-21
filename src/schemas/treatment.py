import datetime
import random
from typing import List, Literal

from pydantic import BaseModel

"""         ----- Measurements -----         """


class MeasurementAddUpdateSchema(BaseModel):
    date: datetime.datetime
    type: str
    value: str

    class Config:
        schema_extra = {
            "example": {
                "date": "2021-01-01T00:00:00",
                "type": "Glucosa",
                "value": "120",
            }
        }


class MeasurementSchema(MeasurementAddUpdateSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": random.randint(1000, 10000),
                **MeasurementAddUpdateSchema.Config.schema_extra["example"],
            }
        }


"""         ----- Consumption -----         """


class ConsumptionRule(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    hours: List[str] | None
    days: List[
        Literal[
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        ]
    ] | None
    everyxdays: int | None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "start": "2021-01-01 00:00:00",
                "end": "2021-01-31 00:00:00",
                "hours": ["00:00", "12:00"],
                "days": ["monday", "tuesday", "wednesday", "thursday"],
                "everyxdays": None,
            }
        }


class ConsumptionSchema(BaseModel):
    datetime: datetime.datetime
    consumed: bool

    class Config:
        schema_extra = {
            "example": {
                "datetime": datetime.datetime.now(),
                "consumed": True,
            }
        }


"""         ----- Medicine -----         """


class MedicineSchema(BaseModel):
    name: str
    icon: str
    application: str
    presentation: str
    dosis_unit: str
    dosis: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": random.choice(
                    ["Paracetamol", "Ibuprofeno", "Diazepam", "Cafalexina"]
                ),
                "icon": "https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png",
                "application": random.choice(["oral", "intravenous", "intramuscular"]),
                "presentation": random.choice(["pastilla", "solución", "inyección"]),
                "dosis_unit": random.choice(["mg", "ml", "gr"]),
                "dosis": random.randint(1, 10),
            }
        }


"""         ----- Treatment -----         """


class TreatmentAddUpdateSchema(BaseModel):
    medicine: MedicineSchema
    consumption_rule: ConsumptionRule

    stock: int | None
    stock_warning: int | None
    instructions: str | None

    class Config:
        # TODO: Mejorar estos ejemplos
        schema_extra = {
            "example": {
                "medicine": MedicineSchema.Config.schema_extra["example"],
                "consumption_rule": ConsumptionRule.Config.schema_extra["example"],
                "stock": random.randint(15, 50),
                "stock_warning": random.randint(5, 10),
                "instructions": "Tomarlo cada 8 hs",
            }
        }


class TreatmentSchema(TreatmentAddUpdateSchema):
    id: int
    consumptions: List[ConsumptionSchema]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": random.randint(1000, 10000),
                "consumptions": [
                    ConsumptionSchema.Config.schema_extra["example"],
                ],
                **TreatmentAddUpdateSchema.Config.schema_extra["example"],
            }
        }


"""         ----- New Consumption -----         """


class NewConsumption(BaseModel):
    consumption_date: datetime.datetime
