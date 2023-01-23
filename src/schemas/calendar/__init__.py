from pydantic import BaseModel

from schemas.calendar.appointment import AppointmentSchema
from schemas.calendar.measurement import MeasurementSchema
from schemas.calendar.medicine import ConsumptionSchema, MedicineSchema


class CalendarSchema(BaseModel):
    consumptions: list[ConsumptionSchema]
    appointments: list[AppointmentSchema]
    measurements: list[MeasurementSchema]
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
                "measurements": [
                    MeasurementSchema.Config.schema_extra["example"],
                    MeasurementSchema.Config.schema_extra["example"],
                    MeasurementSchema.Config.schema_extra["example"],
                ],
                "active_medicines": [
                    MedicineSchema.Config.schema_extra["example"],
                    MedicineSchema.Config.schema_extra["example"],
                    MedicineSchema.Config.schema_extra["example"],
                ],
            }
        }