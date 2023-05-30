import datetime

from dateutil.rrule import DAILY, WEEKLY, rrule
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from api.medicine.exceptions import (
    IncorrectHourFormat,
    IntervalAndDays,
    InvalidDate,
    InvalidHour,
    NoHourSelected,
)
from models import CRUD


class Consumption(CRUD):
    __tablename__ = "consumption"

    id = None  # Replace the id column with the date column
    date = Column(DateTime, primary_key=True)
    real_consumption_date = Column(DateTime)

    medicine_id = Column(
        Integer, ForeignKey("medicine.id", ondelete="CASCADE"), primary_key=True
    )
    medicine = relationship(
        "Medicine", backref="consumptions", foreign_keys=[medicine_id]
    )

    def validate(self):
        frequency = self.medicine.get_frequency()
        if not frequency:
            return
        only_date = self.date.date()
        only_date = datetime.datetime(only_date.year, only_date.month, only_date.day)
        only_hour = self.date.time().strftime("%H:%M")
        if only_date not in frequency:
            raise InvalidDate
        if only_hour not in self.medicine.hours:
            raise InvalidHour


class Medicine(CRUD):
    __tablename__ = "medicine"

    name = Column(String(255), nullable=False, index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean, nullable=False, server_default=expression.true())

    stock = Column(Integer, nullable=True)
    stock_warning = Column(Integer, nullable=True)

    presentation = Column(
        String(255), nullable=False
    )  # Pastilla, Cápsula, Líquido, etc.
    dosis_unit = Column(String(10), nullable=False)  # mg, ml, etc.
    dosis = Column(Float, nullable=False)  # 500, 1, etc.

    interval = Column(Integer, nullable=True)  # Cada 4 dias
    days = Column(
        ARRAY(Integer), nullable=True
    )  # [1, 3, 5] -> Lunes, Miércoles, Viernes
    hours = Column(
        ARRAY(String), nullable=True
    )  # ["12:00", "18:30", "22:00"] -> 12:00, 18:30, 22:00

    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="medicines", foreign_keys=[user_id])

    instructions = Column(String(255), nullable=True)

    def validate(self):
        if self.interval and self.days:
            raise IntervalAndDays
        if self.interval or self.days:
            if not self.hours or len(self.hours) == 0:
                raise NoHourSelected
            for hour in self.hours:
                try:
                    datetime.datetime.strptime(hour, "%H:%M")
                except ValueError:
                    raise IncorrectHourFormat

    def get_frequency(self):
        if not self.hours:
            return None
        if self.interval:
            frequency = rrule(
                DAILY,
                interval=self.interval,
                dtstart=self.start_date.date(),
                until=self.end_date.date() if self.end_date else None,
            )
        else:
            frequency = rrule(
                WEEKLY,
                byweekday=self.days,
                dtstart=self.start_date.date(),
                until=self.end_date.date() if self.end_date else None,
            )
        return frequency
