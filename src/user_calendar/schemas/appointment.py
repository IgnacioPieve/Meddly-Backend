import datetime

from pydantic import BaseModel


class AddAppointmentSchema(BaseModel):
    date: datetime.datetime
    name: str

    doctor: str | None
    speciality: str | None
    location: str | None
    notes: str | None

    class Config:
        schema_extra = {
            "example": {
                "date": datetime.datetime(2023, 1, 10),
                "name": "Consulta con Cardiólogo",
                "doctor": "Dr. Juan Perez",
                "speciality": "Cardiología",
                "location": "Hospital de la ciudad",
                "notes": "Llevar los resultados de los análisis",
            }
        }


class AppointmentSchema(AddAppointmentSchema):
    id: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 123456789,
                **AddAppointmentSchema.Config.schema_extra["example"],
            }
        }
