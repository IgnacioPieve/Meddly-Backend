import datetime
import random
from typing import Dict, List, Literal

from pydantic import BaseModel

"""         ----- Consumption -----         """


class ConsumptionHourSchema(BaseModel):
    hour: str
    consumed: bool


class ConsumptionSchema(BaseModel):
    __root__: Dict[str, List[ConsumptionHourSchema]]

    class Config:
        schema_extra = {
            "example": {
                "2022-08-14": [{"hour": "16:43", "consumed": False}],
                "2022-08-17": [{"hour": "16:43", "consumed": True}],
                "2022-08-20": [{"hour": "16:43", "consumed": False}],
                "2022-08-23": [{"hour": "16:43", "consumed": True}],
            }
        }


"""         ----- Consumption Rules -----         """


class ConsumptionRuleSchema(BaseModel):
    start: datetime.datetime
    end: datetime.datetime | None
    runtimeType: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "start": datetime.datetime.now(),
                "end": datetime.datetime.now()
                + datetime.timedelta(days=random.randint(10, 20)),
            }
        }


class NeedItSchema(ConsumptionRuleSchema):
    """
    Esta regla se aplica cuando el usuario indica que necesita consumir el medicamento
    """

    runtimeType: Literal["need_it"]

    class Config:
        schema_extra = {
            "example": {
                "runtimeType": "need_it",
                **ConsumptionRuleSchema.Config.schema_extra["example"],
            }
        }


class EveryDaySchema(ConsumptionRuleSchema):
    """
    Esta regla de consumo se aplica todos los días, por ejemplo:
        Si el medicamento se debe aplicar todos los días a las 11.00 y a las 23.00 (hours = [11.00, 23.00]),
        a partir del Lunes 1 de Junio, las próximas fechas válidas para aplicar el medicamento son:
            - Martes 2 de Junio a las 11.00 y luego las 23.00
            - Miércoles 3 de Junio a las 11.00 y luego las 23.00
            - Jueves 4 de Junio a las 11.00 y luego las 23.00
            - Viernes 5 de Junio a las 11.00 y luego las 23.00
            - etc...
    """

    runtimeType: Literal["every_day"]
    hours: list[datetime.time]

    class Config:
        schema_extra = {
            "example": {
                "runtimeType": "every_day",
                "hours": random.sample(
                    [
                        f"0{random.randint(1, 9)}:00",
                        f"{random.randint(10, 15)}:00",
                        f"{random.randint(16, 20)}:00",
                        f"{random.randint(21, 23)}:00",
                    ],
                    random.randint(1, 4),
                ),
                **ConsumptionRuleSchema.Config.schema_extra["example"],
            }
        }


class EveryXDaySchema(ConsumptionRuleSchema):
    """
    Esta regla de consumos se aplica cada x días, por ejemplo:
        Si el medicamento se debe aplicar cada 2 días (number = 2), a partir del Lunes 1 de Junio a las 17.30,
        las próximas fechas válidas para aplicar el medicamento son:
            - Miércoles 3 de Junio a las 17.30
            - Viernes 5 de Junio a las 17.30
            - Domingo 7 de Junio a las 17.30
            - etc...
    """

    runtimeType: Literal["every_x_day"]
    number: int

    class Config:
        schema_extra = {
            "example": {
                "runtimeType": "every_x_day",
                "number": random.randint(2, 5),
                **ConsumptionRuleSchema.Config.schema_extra["example"],
            }
        }


class SpecificDaysSchema(ConsumptionRuleSchema):
    """
    Esta regla de consumo se aplica en días específicos, por ejemplo:
        Si el medicamento se debe aplicar los días Martes, Jueves y Sábado (days = ["tuesday", "thursday", "saturday"]), a partir del Martes 2 de Junio a las 17.30,
        las próximas fechas válidas para aplicar el medicamento son:
            - Jueves 4 de Junio a las 17.30
            - Sábado 6 de Junio a las 17.30
            - Martes 9 de Junio a las 17.30
            - etc...
    """

    runtimeType: Literal["specific_days"]
    days: list[
        Literal[
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"
        ]
    ]

    class Config:
        schema_extra = {
            "example": {
                "runtimeType": "specific_days",
                "days": random.sample(
                    [
                        "monday",
                        "tuesday",
                        "wednesday",
                        "thursday",
                        "friday",
                        "saturday",
                        "sunday",
                    ],
                    random.randint(1, 7),
                ),
                **ConsumptionRuleSchema.Config.schema_extra["example"],
            }
        }


"""         ----- Medicine -----         """


class MethodSchema(BaseModel):
    name: str
    runtimeType: str

    class Config:
        orm_mode = True


class MedicineDosisSchema(MethodSchema):
    runtimeType: Literal["dosis"]
    value: float
    unit: str


class MedicineApplicationSchema(MethodSchema):
    runtimeType: Literal["application"]
    description: str


class MedicineSchema(BaseModel):
    name: str
    icon: str
    method: MedicineDosisSchema | MedicineApplicationSchema

    class Config:
        orm_mode = True


"""         ----- Treatment -----         """


class TreatmentIndicationSchema(BaseModel):
    consumption_rule: NeedItSchema | EveryDaySchema | EveryXDaySchema | SpecificDaysSchema
    instructions: str | None

    class Config:
        orm_mode = True
        example_instructions = [
            "Tomarlo cada 8 horas",
            "Tomarlo al despertarme",
            "Inyectar antes de ir a dormir",
        ]
        schema_extra = {
            "example": {
                "consumption_rule": random.choice(
                    [NeedItSchema, EveryDaySchema, EveryXDaySchema, SpecificDaysSchema]
                ).Config.schema_extra["example"],
                "instructions": random.choice(example_instructions),
            }
        }


class TreatmentAddUpdateSchema(BaseModel):
    medicine: MedicineSchema
    treatment_indication: TreatmentIndicationSchema

    stock: int | None
    stock_warning: int | None

    class Config:
        # TODO: Mejorar estos ejemplos
        schema_extra = {
            "example": {
                "medicine": {
                    "name": random.choice(
                        ["Paracetamol", "Ibuprofeno", "Diazepam", "Cafalexina"]
                    ),
                    "icon": "https://www.google.com/",
                    "method": {
                        "name": "Pastilla",
                        "runtimeType": "dosis",
                        "value": 10,
                        "unit": "mg",
                    },
                },
                "treatment_indication": TreatmentIndicationSchema.Config.schema_extra[
                    "example"
                ],
                "stock": random.randint(15, 50),
                "stock_warning": random.randint(5, 10),
            }
        }


class TreatmentSchema(TreatmentAddUpdateSchema):
    id: int
    consumptions: ConsumptionSchema

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
