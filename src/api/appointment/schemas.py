import datetime

from pydantic import BaseModel


class CreateUpdateAppointmentSchema(BaseModel):
    date: datetime.datetime
    name: str

    doctor: str | None
    speciality: str | None
    location: str | None
    notes: str | None

    class Config:
        schema_extra = {
            "example": {
                "date": datetime.datetime.now(),
                "name": "Consulta con Cardiólogo",
                "doctor": "Dr. Juan Perez",
                "speciality": "Cardiología",
                "location": "Hospital de la ciudad",
                "notes": "Llevar los resultados de los análisis",
            }
        }


class AppointmentSchema(CreateUpdateAppointmentSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 123456789,
                **CreateUpdateAppointmentSchema.Config.schema_extra["example"],
            }
        }
