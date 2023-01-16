from schemas.calendar.medicine import *
from schemas.calendar.appointment import *


class CalendarSchema(BaseModel):
    consumptions: list[ConsumptionSchema]
    appointments: list[AppointmentSchema]
    active_medicines: list[MedicineSchema]

    class Config:
        schema_extra = {
            "example": {
                "consumptions": [
                    ConsumptionSchema.Config.schema_extra["example"],
                    ConsumptionSchema.Config.schema_extra["example"],
                    ConsumptionSchema.Config.schema_extra["example"],
                ],
                "appointments": [
                    AppointmentSchema.Config.schema_extra["example"],
                    AppointmentSchema.Config.schema_extra["example"],
                    AppointmentSchema.Config.schema_extra["example"],
                ],
                "active_medicines": [
                    MedicineSchema.Config.schema_extra["examples"]["every_week"],
                    MedicineSchema.Config.schema_extra["examples"]["interval"],
                    MedicineSchema.Config.schema_extra["examples"]["when_need"],
                ],
            }
        }
