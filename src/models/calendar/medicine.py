import datetime

from dateutil.rrule import DAILY, WEEKLY, rrule
from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    PickleType,
    String,
)
from sqlalchemy.orm import relationship
from whoosh import index
from whoosh.qparser import QueryParser

from models.utils import CRUD, raise_errorcode

medicines_index = index.open_dir("indexes/medicines_index")
searcher = medicines_index.searcher()
query_parser = QueryParser("description", schema=medicines_index.schema)


class Consumption(CRUD):
    __tablename__ = "consumption"

    date = Column(DateTime, primary_key=True)
    real_consumption_date = Column(DateTime)

    # ondelete cascade
    medicine_id = Column(Integer, ForeignKey("medicine.id"), primary_key=True)
    medicine = relationship(
        "Medicine", backref="consumptions", foreign_keys=[medicine_id]
    )

    def validate_day(self, consumption_date: datetime.datetime):
        frequency = self.medicine.get_frequency()
        if not frequency:
            return
        only_date = consumption_date.date()
        only_date = datetime.datetime(only_date.year, only_date.month, only_date.day)
        only_hour = consumption_date.time().strftime("%H:%M")
        if only_date not in frequency:
            raise_errorcode(302)
        if only_hour not in self.medicine.hours:
            raise_errorcode(303)

    def create(self):
        self.validate_day(self.date)
        self.medicine.stock -= 1 if self.medicine.stock > 0 else 0
        return super().create()

    def destroy(self):
        self.medicine.stock += 1
        return super().destroy()


class Medicine(CRUD):
    __tablename__ = "medicine"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    stock = Column(Integer, nullable=True)
    stock_warning = Column(Integer, nullable=True)

    presentation = Column(
        String(255), nullable=False
    )  # Pastilla, Cápsula, Líquido, etc.
    dosis_unit = Column(String(10), nullable=False)  # mg, ml, etc.
    dosis = Column(Float, nullable=False)  # 500, 1, etc.

    interval = Column(Integer, nullable=True)  # Cada 4 dias
    days = Column(PickleType(), nullable=True)  # [1, 3, 5] -> Lunes, Miércoles, Viernes
    hours = Column(
        PickleType(), nullable=True
    )  # ["12:00", "18:30", "22:00"] -> 12:00, 18:30, 22:00

    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="medicines", foreign_keys=[user_id])

    instructions = Column(String(255), nullable=True)

    def validate(self):
        if self.interval and self.days:
            raise_errorcode(300)
        if self.interval or self.days:
            if not self.hours or len(self.hours) == 0:
                raise_errorcode(301)
            for hour in self.hours:
                try:
                    datetime.datetime.strptime(hour, "%H:%M")
                except ValueError:
                    raise_errorcode(304)

    def get_frequency(self):
        if not self.hours:
            return None
        if self.interval:
            frequency = rrule(
                DAILY,
                interval=self.interval,
                dtstart=self.start_date,
                until=self.end_date,
            )
        else:
            frequency = rrule(
                WEEKLY,
                byweekday=self.days,
                dtstart=self.start_date,
                until=self.end_date,
            )
        return frequency

    def get_consumptions(self, start: datetime.datetime, end: datetime.datetime, db):
        consumptions = []
        consumptions_taken = {
            c.date: c for c in self.consumptions if start <= c.date <= end
        }
        if self.hours:
            for date in self.get_frequency().between(
                start,
                end,
            ):
                for hour in self.hours:
                    date_hour = datetime.datetime.combine(
                        date, datetime.datetime.strptime(hour, "%H:%M").time()
                    )
                    if date_hour not in consumptions_taken:
                        c = Consumption(
                            db,
                            date=date_hour,
                            real_consumption_date=date_hour,
                            medicine=self,
                            medicine_id=self.id,
                            created_at=datetime.datetime.now(),
                            updated_at=datetime.datetime.now(),
                        )
                        c.consumed = False
                    else:
                        c = consumptions_taken[date_hour]
                        c.consumed = True
                    consumptions.append(c)
        return consumptions

    def destroy(self):
        for consumption in self.consumptions:
            consumption.db = self.db
            consumption.destroy()
        return super().destroy()

    @staticmethod
    def search(query):
        results = searcher.search(query_parser.parse(f"{query.strip()}*"))
        return [
            {"code": result["code"], "description": result["description"]}
            for result in results
        ]
