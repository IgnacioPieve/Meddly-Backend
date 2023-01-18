import datetime

from pydantic import BaseModel


class AddMeasurementSchema(BaseModel):
    date: datetime.datetime
    type: str
    value: float

    class Config:
        schema_extra = {
            "example": {
                "date": datetime.datetime(2023, 1, 10),
                "type": "Glucosa",
                "value": 95.0,
            }
        }


class MeasurementSchema(AddMeasurementSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 123456789,
                **AddMeasurementSchema.Config.schema_extra["example"],
            }
        }
