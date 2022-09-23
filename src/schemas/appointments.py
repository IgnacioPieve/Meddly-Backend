import datetime
import random

from pydantic import BaseModel

"""         ----- Appointments -----         """


class AppointmentAddUpdateSchema(BaseModel):
    date: datetime.datetime
    doctor: str | None
    speciality: str | None
    location: str | None
    notes: str | None

    class Config:
        schema_extra = {
            "example": {
                "date": "2021-01-01T00:00:00",
                "doctor": "Dr. House",
                "speciality": "Cardiología",
                "location": "Hospital General",
                "notes": "Examen de Próstata",
            }
        }


class AppointmentSchema(AppointmentAddUpdateSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": random.randint(1000, 10000),
                **AppointmentAddUpdateSchema.Config.schema_extra["example"],
            }
        }
