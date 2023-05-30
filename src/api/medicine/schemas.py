from datetime import datetime, timedelta
from typing import List, Literal

from pydantic import BaseModel

example_date = datetime.now().replace(hour=10, minute=30, second=0, microsecond=0)


class CreateMedicineSchema(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime | None
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
        schema_extra = {
            "example": {
                "name": "Ibuprofeno",
                "start_date": example_date,
                "end_date": example_date + timedelta(days=30),
                "stock": 18,
                "stock_warning": 5,
                "presentation": "Pastilla",
                "dosis_unit": "mg",
                "dosis": 1.5,
                "instructions": "Disolver la pastilla en agua",
                "interval": 2,
                "hours": ["08:00", "11:30", "18:00"],
            }
        }


class MedicineSchema(CreateMedicineSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 123456789,
                **CreateMedicineSchema.Config.schema_extra["example"],
            }
        }


class CreateConsumptionSchema(BaseModel):
    date: datetime
    real_consumption_date: datetime
    medicine_id: int

    class Config:
        schema_extra = {
            "example": {
                "date": example_date.replace(hour=11, minute=30),
                "real_consumption_date": example_date + timedelta(minutes=30),
                "medicine_id": 123456789,
            }
        }


class DeleteConsumptionSchema(BaseModel):
    date: datetime
    real_consumption_date: datetime | None
    medicine_id: int

    class Config:
        schema_extra = {
            "example": {
                "date": example_date.replace(hour=11, minute=30),
                "medicine_id": 123456789,
            }
        }


class ConsumptionSchema(CreateConsumptionSchema):
    consumed: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                **CreateConsumptionSchema.Config.schema_extra["example"],
                "consumed": True,
            }
        }
