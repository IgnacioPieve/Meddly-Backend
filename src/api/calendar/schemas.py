from typing import Dict

from pydantic import BaseModel

from api.appointment.schemas import AppointmentSchema
from api.measurement.schemas import MeasurementSchema
from api.medicine.schemas import ConsumptionSchema, MedicineSchema


class UserCalendarSchema(BaseModel):
    consumptions: list[ConsumptionSchema]
    appointments: list[AppointmentSchema]
    measurements: list[MeasurementSchema]
    medicines: list[MedicineSchema]

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
                "medicines": [
                    MedicineSchema.Config.schema_extra["example"],
                    MedicineSchema.Config.schema_extra["example"],
                    MedicineSchema.Config.schema_extra["example"],
                ],
            }
        }


class CalendarSchema(BaseModel):
    __root__: Dict[str, UserCalendarSchema]

    class Config:
        schema_extra = {
            "example": {
                "9Tpn37F9xsNSTZpHU0WIrv8PUfl2": {
                    **UserCalendarSchema.Config.schema_extra["example"]
                },
                "wMA6wR4fqgfsAgXr7gokJ3I2ak73": {
                    **UserCalendarSchema.Config.schema_extra["example"]
                },
                "v097YYUZQmTCeLYEFrUNisv3qbg2": {
                    **UserCalendarSchema.Config.schema_extra["example"]
                },
            }
        }
