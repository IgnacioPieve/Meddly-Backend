from pydantic import BaseModel

from api.appointment.schemas import AppointmentSchema
from api.measurement.schemas import MeasurementSchema
from api.medicine.schemas import ConsumptionSchema


class CalendarSchema(BaseModel):
    consumptions: list[ConsumptionSchema]
    appointments: list[AppointmentSchema]
    measurements: list[MeasurementSchema]

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
            }
        }
