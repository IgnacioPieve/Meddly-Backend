from datetime import datetime

from pydantic import BaseModel


class CreateUpdateMeasurementSchema(BaseModel):
    date: datetime
    type: str
    value: float
    unit: str

    class Config:
        schema_extra = {
            "example": {
                "date": datetime.now(),
                "type": "Glucosa",
                "value": 95.0,
                "unit": "mg/dl",
            }
        }


class MeasurementSchema(CreateUpdateMeasurementSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 123456789,
                **CreateUpdateMeasurementSchema.Config.schema_extra["example"],
            }
        }
