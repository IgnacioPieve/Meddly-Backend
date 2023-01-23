import datetime
import threading

from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String, and_)
from sqlalchemy.orm import relationship

from models.message import Message, NewSupervisorMessage, NewSupervisedMessage
from models.utils import CRUD, generate_code, raise_errorcode


class Supervised(CRUD):
    __tablename__ = "supervised"
    id = Column(Integer, primary_key=True, index=True)
    supervisor_id = Column(
        String(255), ForeignKey("user.id"), nullable=False, index=True
    )
    supervisor = relationship(
        "User", backref="supervised_list", foreign_keys=[supervisor_id]
    )
    supervised_id = Column(
        String(255), ForeignKey("user.id"), nullable=False, index=True
    )
    supervised = relationship(
        "User", backref="supervisors_list", foreign_keys=[supervised_id]
    )


class User(CRUD):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    invitation = Column(String(255), nullable=False, index=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    sex = Column(Boolean, nullable=True)
    birth = Column(DateTime, nullable=True)
    phone = Column(String(20), nullable=True)

    def create(self):
        self.invitation = generate_code()
        return super().create()

    def accept_invitation(self, invitation_code):
        supervisor = User(self.db, User.invitation == invitation_code).get()
        if supervisor is None:
            raise_errorcode(201)
        if supervisor.id == self.id:
            raise_errorcode(204)
        already_supervised = (
                Supervised(
                    self.db,
                    and_(Supervised.supervisor == supervisor, Supervised.supervised == self),
                ).get()
                is not None
        )
        if already_supervised:
            raise_errorcode(200)
        supervisor.invitation = generate_code()

        supervisor.save()
        Supervised(self.db, supervisor=supervisor, supervised=self).create()

        self.send_notification(NewSupervisorMessage(supervisor=supervisor))
        supervisor.send_notification(NewSupervisedMessage(supervised=self))

    @property
    def notification_preferences(self):
        return [str(preference) for preference in self.notification_preferences_list]

    def send_notification(self, message: Message):
        for notification_preference in self.notification_preferences_list:
            thread = threading.Thread(
                target=notification_preference.send_notification, args=(message,)
            )
            thread.start()

    def get_calendar(self, start: datetime.date, end: datetime.date):
        calendar = {
            "consumptions": [],
            "appointments": [],
            "measurements": [],
            "active_medicines": [],
        }
        # Get appointments
        for appointment in self.appointments:
            if start <= appointment.date.date() <= end:
                calendar["appointments"].append(appointment)

        # Get measurements
        for measurement in self.measurements:
            if start <= measurement.date.date() <= end:
                calendar["measurements"].append(measurement)

        # Get active_medicines and consumptions
        for medicine in self.medicines:
            if medicine.active:
                calendar["active_medicines"].append(medicine)
            if medicine.start_date > end or (
                    medicine.end_date and medicine.end_date < start
            ):
                continue
            calendar["consumptions"] += medicine.get_consumptions(start, end, self.db)
        return calendar
