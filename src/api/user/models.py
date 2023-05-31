import datetime
import threading

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, and_, func
from sqlalchemy.orm import relationship

from api.notification.models.message import (
    Message,
    NewSupervisedMessage,
    NewSupervisorMessage,
)
from api.supervisor.exceptions import ERROR200, ERROR201, ERROR204
from models import CRUD

base_date = datetime.datetime(1900, 1, 1)
final_date = datetime.datetime(2100, 1, 1)


class Supervised(CRUD):
    __tablename__ = "supervised"
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

    def accept_invitation(self, invitation_code):
        supervisor = User(self.db, User.invitation == invitation_code).get()
        if supervisor is None:
            raise ERROR201
        if supervisor.id == self.id:
            raise ERROR204
        already_supervised = (
            Supervised(
                self.db,
                and_(
                    Supervised.supervisor == supervisor, Supervised.supervised == self
                ),
            ).get()
            is not None
        )
        if already_supervised:
            raise ERROR200
        supervisor.invitation = """generate_code()"""

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

    def get_age(self):
        today = datetime.date.today()
        return (
            today.year
            - self.birth.year
            - ((today.month, today.day) < (self.birth.month, self.birth.day))
        )

    def get_fullname(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.last_name:
            return self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return self.email.split("@")[0]

    def get_birth_text(self):
        if self.birth:
            months = [
                "enero",
                "febrero",
                "marzo",
                "abril",
                "mayo",
                "junio",
                "julio",
                "agosto",
                "septiembre",
                "octubre",
                "noviembre",
                "diciembre",
            ]
            return f"{self.birth.day} de {months[self.birth.month - 1]} del {self.birth.year}"
        else:
            return None


class Device(CRUD):
    __tablename__ = "device"

    user_id = Column(String(255), ForeignKey("user.id"), nullable=False, index=True)
    user = relationship("User", backref="devices", foreign_keys=[user_id])
    token = Column(String(255), nullable=False, index=True)
    last_access = Column(
        DateTime, server_default=func.now(), nullable=False, index=True
    )
