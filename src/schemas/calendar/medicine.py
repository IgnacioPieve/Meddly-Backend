import datetime
from typing import List, Literal

from pydantic import BaseModel


class MedicineAddSchema(BaseModel):
    name: str
    start_date: datetime.date
    end_date: datetime.date | None
    stock: int | None
    stock_warning: int | None
    presentation: str
    dosis_unit: str
    dosis: float
    interval: int | None
    days: List[Literal[1, 2, 3, 4, 5, 6, 7]] | None
    hours: List[str] | None
    instructions: str | None

    class Config:
        basic_example = {
            "name": "Ibuprofeno",
            "start_date": datetime.datetime(2023, 1, 10),
            "end_date": datetime.datetime(2023, 2, 1),
            "stock": 18,
            "stock_warning": 5,
            "presentation": "Pastilla",
            "dosis_unit": "mg",
            "dosis": 1.5,
            "instructions": "Disolver la pastilla en agua",
        }
        schema_extra = {
            "examples": {
                "every_week": {
                    **basic_example,
                    "days": [1, 3, 5],
                    "hours": ["08:00", "11:30", "18:00"],
                },
                "interval": {
                    **basic_example,
                    "interval": 2,
                    "hours": ["08:00", "11:30", "18:00"],
                },
                "when_need": basic_example,
            }
        }


class MedicineSchema(MedicineAddSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "examples": {
                "every_week": {
                    "id": 123456789,
                    **MedicineAddSchema.Config.schema_extra["examples"]["every_week"],
                },
                "interval": {
                    "id": 123456789,
                    **MedicineAddSchema.Config.schema_extra["examples"]["interval"],
                },
                "when_need": {
                    "id": 123456789,
                    **MedicineAddSchema.Config.schema_extra["examples"]["when_need"],
                },
            }
        }


class AddConsumptionSchema(BaseModel):
    date: datetime.datetime
    real_consumption_date: datetime.datetime
    medicine_id: int

    class Config:
        schema_extra = {
            "example": {
                "date": datetime.datetime(2023, 1, 10, 8, 0),
                "real_consumption_date": datetime.datetime(2023, 1, 10, 9, 35),
                "medicine_id": 123456789,
            }
        }


class ConsumptionSchema(AddConsumptionSchema):
    consumed: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                **AddConsumptionSchema.Config.schema_extra["example"],
                "consumed": True,
            }
        }
