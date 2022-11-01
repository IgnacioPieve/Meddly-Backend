import calendar
import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import backref, relationship

from config import translations
from models.message import LowStockMessage
from models.utils import CRUD


class Measurement(CRUD):
    __tablename__ = "measurement"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    type = Column(String, nullable=False)
    value = Column(String, nullable=False)
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="measurements", foreign_keys=[user_id])


# ----- CONSUMPTION -----
class Consumption(CRUD):
    __tablename__ = "consumption"

    datetime = Column(DateTime, primary_key=True)
    treatment_id = Column(Integer, ForeignKey("treatment.id"), primary_key=True)
    treatment = relationship(
        "Treatment", backref=backref("consumption_list", cascade="all, delete-orphan")
    )

    def create(self):
        super().create()

        if (
            self.treatment.stock_warning
            and self.treatment.stock
            and self.treatment.stock <= self.treatment.stock_warning
        ):
            m = LowStockMessage()
            self.treatment.user.send_notification(m)
        if self.treatment.stock:
            self.treatment.stock -= 1 if self.treatment.stock > 0 else 0
        self.treatment.save()

        return self

    def destroy(self):
        if self.treatment.stock:
            self.treatment.stock += 1
        return super().destroy()


# ----- MEDICINE -----
class Medicine(CRUD):
    __tablename__ = "medicine"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    icon = Column(String(255), nullable=False)
    application = Column(String(255), nullable=True)
    presentation = Column(String(255), nullable=True)
    dosis_unit = Column(String(255), nullable=True)
    dosis = Column(Float, nullable=True)


# ----- CONSUMPTION RULE -----
class ConsumptionRule(CRUD):
    __tablename__ = "consumption_rule"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)
    hours = Column(PickleType(), nullable=True)
    days = Column(PickleType(), nullable=True)
    everyxdays = Column(Integer, nullable=True)

    def validate_consumption(self, consumption: datetime.datetime):
        if self.validate_date_range(consumption) == "start":
            raise translations["errors"]["treatments"][
                "consumption_before_treatment_start"
            ]
        elif self.validate_date_range(consumption) == "end":
            raise translations["errors"]["treatments"]["treatment_expired"]
        if not self.validate_day(consumption):
            raise translations["errors"]["treatments"]["incorrect_date"]
        if not self.validate_hour(consumption):
            raise translations["errors"]["treatments"]["incorrect_time"]

    def validate_day(self, consumption: datetime.datetime):
        if self.everyxdays is not None:
            correct_day = (
                relativedelta(
                    self.start,
                    datetime.datetime(
                        consumption.year,
                        consumption.month,
                        consumption.day,
                        self.start.hour,
                        self.start.minute,
                        self.start.second,
                    ),
                ).days
                % self.everyxdays
            ) == 0
        else:
            correct_day = calendar.day_name[consumption.weekday()].lower() in self.days
        return correct_day

    def validate_hour(self, consumption: datetime.datetime):
        hour = f"{consumption.hour:02d}:{consumption.minute:02d}"
        correct_hour = hour in self.hours
        # TODO: el if y return se puede hacer en una sola linea
        if not correct_hour:
            return False
        return True

    def validate_date_range(self, consumption: datetime.datetime):
        if consumption < self.start:
            return "start"
        if self.end is not None and consumption > self.end:
            return "end"
        return True

    def get_proyections(self, start: datetime.datetime, end: datetime.datetime):
        proyections = {}
        days = [
            start + datetime.timedelta(days=x) for x in range((end - start).days + 1)
        ]
        for day in days:
            correct_day = self.validate_day(day)
            correct_range = self.validate_date_range(day)
            if correct_day and (correct_range is True):
                proyections[day.strftime("%Y-%m-%d")] = self.hours

        return proyections


# ----- TREATMENT -----
class Treatment(CRUD):
    __tablename__ = "treatment"
    id = Column(Integer, primary_key=True, index=True)
    stock = Column(Integer, nullable=True)
    stock_warning = Column(Integer, nullable=True)

    medicine_id = Column(Integer, ForeignKey("medicine.id"), index=True, nullable=False)
    medicine = relationship(Medicine, backref="treatment", foreign_keys=[medicine_id])
    consumption_rule_id = Column(
        Integer, ForeignKey("consumption_rule.id"), index=True, nullable=False
    )
    consumption_rule = relationship(
        ConsumptionRule, backref="treatment", foreign_keys=[consumption_rule_id]
    )
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="treatments", foreign_keys=[user_id])
    instructions = Column(String(255), nullable=True)

    @property
    def consumptions(self):
        start_datetime = datetime.datetime.now() - datetime.timedelta(days=15)
        end_datetime = datetime.datetime.now() + datetime.timedelta(days=15)

        proyections = self.consumption_rule.get_proyections(
            start=start_datetime, end=end_datetime
        )

        consumptions_dict = {}
        for consumption in self.consumption_list:
            if start_datetime <= consumption.datetime <= end_datetime:
                if consumption.datetime.strftime("%Y-%m-%d") not in consumptions_dict:
                    consumptions_dict[consumption.datetime.strftime("%Y-%m-%d")] = []
                consumptions_dict[consumption.datetime.strftime("%Y-%m-%d")].append(
                    consumption.datetime.strftime("%H:%M")
                )

        proyection_with_consumptions = {}
        for day in proyections:
            proyection_with_consumptions[day] = []
            for hour in proyections[day]:
                consumed = False
                if day in consumptions_dict and hour in consumptions_dict[day]:
                    consumed = True

                proyection_with_consumptions[day].append(
                    {"hour": hour, "consumed": consumed}
                )

        proyections_array = []
        for day in proyection_with_consumptions:
            for consumption in proyection_with_consumptions[day]:
                proyections_array.append(
                    {
                        "datetime": datetime.datetime.strptime(
                            day + " " + consumption["hour"], "%Y-%m-%d %H:%M"
                        ),
                        "consumed": consumption["consumed"],
                    }
                )
        return proyections_array
