import calendar
import datetime

from dateutil.relativedelta import relativedelta
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer,
                        PickleType, String)
from sqlalchemy.orm import relationship

from config import translations
from models.utils import CRUD


# ----- CONSUMPTION -----
class Consumption(CRUD):
    __tablename__ = "consumption"

    datetime = Column(DateTime, primary_key=True)
    treatment_id = Column(Integer, ForeignKey("treatment.id"), primary_key=True)
    treatment = relationship("Treatment", backref="consumption_list")


# ----- MEDICINE -----
class Method(CRUD):
    __tablename__ = "method"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    __mapper_args__ = {"polymorphic_on": type}


class MedicineApplication(Method):
    __mapper_args__ = {"polymorphic_identity": "application"}

    description = Column(String)


class MedicineDosis(Method):
    __mapper_args__ = {"polymorphic_identity": "dosis"}

    value = Column(Float)
    unit = Column(String)


class Medicine(CRUD):
    __tablename__ = "medicine"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=False)
    method_id = Column(Integer, ForeignKey("method.id"), index=True, nullable=False)
    method = relationship(Method, backref="medicine", foreign_keys=[method_id])


# ----- TREATMENT_INDICATION -----
class ConsumptionRule(CRUD):
    __tablename__ = "consumption_rule"

    id = Column(Integer, primary_key=True, index=True)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=True)
    name = Column(String, nullable=False)
    __mapper_args__ = {"polymorphic_on": name}

    def validate_consumption(self, consumption: datetime.datetime):
        if consumption < self.start:
            raise translations["errors"]["treatments"][
                "consumption_before_treatment_start"
            ]
        if self.end is not None and consumption > self.end:
            raise translations["errors"]["treatments"]["treatment_expired"]

    def get_proyections(self, start: datetime.datetime, end: datetime.datetime):
        return {}


class NeedIt(ConsumptionRule):
    __mapper_args__ = {"polymorphic_identity": "need_it"}

    def validate_consumption(self, consumption: datetime.datetime):
        super().validate_consumption(consumption)
        return


class EveryDay(ConsumptionRule):
    __mapper_args__ = {"polymorphic_identity": "every_day"}

    hours = Column(PickleType())

    def get_proyections(self, start: datetime.datetime, end: datetime.datetime):
        proyections = {}
        days = [
            start + datetime.timedelta(days=x) for x in range((end - start).days + 1)
        ]
        for day in days:
            proyections[day.strftime("%Y-%m-%d")] = []
            for hour in self.hours:
                proyections[day.strftime("%Y-%m-%d")].append(hour.strftime("%H:%M"))
        return proyections

    def validate_consumption(self, consumption: datetime.datetime):
        super().validate_consumption(consumption)

        for hour in self.hours:
            correct_hour = consumption.hour == hour.hour
            correct_minute = consumption.minute == hour.minute
            correct_time = correct_hour and correct_minute
            if correct_time:
                return
        raise translations["errors"]["treatments"]["incorrect_time"]


class EveryXDay(ConsumptionRule):
    __mapper_args__ = {"polymorphic_identity": "every_x_day"}

    number = Column(Integer)

    def get_proyections(self, start: datetime.datetime, end: datetime.datetime):
        proyections = {}
        days = [
            start + datetime.timedelta(days=x) for x in range((end - start).days + 1)
        ]
        for day in days:
            correct_day = (relativedelta(self.start, day).days % self.number) == 0
            if correct_day:
                proyections[day.strftime("%Y-%m-%d")] = [self.start.strftime("%H:%M")]
        return proyections

    def validate_consumption(self, consumption: datetime.datetime):
        super().validate_consumption(consumption)
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
            % self.number
        ) == 0
        if not correct_day:
            raise translations["errors"]["treatments"]["incorrect_date"]
        correct_hour = consumption.hour == self.start.hour
        correct_minute = consumption.minute == self.start.minute
        correct_time = correct_hour and correct_minute
        if not correct_time:
            raise translations["errors"]["treatments"]["incorrect_time"]
        return


class SpecificDays(ConsumptionRule):
    __mapper_args__ = {"polymorphic_identity": "specific_days"}

    days = Column(PickleType())

    def get_proyections(self, start: datetime.datetime, end: datetime.datetime):
        proyections = {}
        days = [
            start + datetime.timedelta(days=x) for x in range((end - start).days + 1)
        ]
        for day in days:
            correct_day = calendar.day_name[day.weekday()].lower() in self.days
            if correct_day:
                proyections[day.strftime("%Y-%m-%d")] = [self.start.strftime("%H:%M")]
        return proyections

    def validate_consumption(self, consumption: datetime.datetime):
        super().validate_consumption(consumption)

        correct_day = calendar.day_name[consumption.weekday()].lower() in self.days

        if not correct_day:
            raise translations["errors"]["treatments"]["incorrect_date"]

        correct_hour = consumption.hour == self.start.hour
        correct_minute = consumption.minute == self.start.minute
        correct_time = correct_hour and correct_minute
        if not correct_time:
            raise translations["errors"]["treatments"]["incorrect_time"]

        return


# ----- TREATMENT -----
class TreatmentIndication(CRUD):
    __tablename__ = "treatment_indication"

    id = Column(Integer, primary_key=True, index=True)
    consumption_rule_id = Column(
        Integer, ForeignKey("consumption_rule.id"), index=True, nullable=False
    )
    consumption_rule = relationship(
        ConsumptionRule,
        backref="treatment_indication",
        foreign_keys=[consumption_rule_id],
    )
    instructions = Column(String, nullable=True)


class Treatment(CRUD):
    __tablename__ = "treatment"
    id = Column(Integer, primary_key=True, index=True)
    stock = Column(Integer, nullable=True)
    stock_warning = Column(Integer, nullable=True)

    medicine_id = Column(Integer, ForeignKey("medicine.id"), index=True, nullable=False)
    medicine = relationship(Medicine, backref="treatment", foreign_keys=[medicine_id])
    treatment_indication_id = Column(
        Integer, ForeignKey("treatment_indication.id"), index=True, nullable=False
    )
    treatment_indication = relationship(
        TreatmentIndication, backref="treatment", foreign_keys=[treatment_indication_id]
    )
    user_id = Column(String, ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="treatments", foreign_keys=[user_id])

    @property
    def consumptions(self):
        start_datetime = datetime.datetime.now() - datetime.timedelta(days=15)
        end_datetime = datetime.datetime.now() + datetime.timedelta(days=15)

        proyections = self.treatment_indication.consumption_rule.get_proyections(
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

        return proyection_with_consumptions