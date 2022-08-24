import threading

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    or_,
)
from sqlalchemy.orm import relationship

from config import translations
from models.message import Message, NewSupervisorMessage
from models.utils import CRUD, generate_code


class Supervised(CRUD):
    __tablename__ = "supervised"
    id = Column(Integer, primary_key=True, index=True)
    supervisor_id = Column(String(255), ForeignKey("user.id"), nullable=False, index=True)
    supervisor = relationship(
        "User", backref="supervised_list", foreign_keys=[supervisor_id]
    )
    supervised_id = Column(String(255), ForeignKey("user.id"), nullable=False, index=True)
    supervised = relationship(
        "User", backref="supervisors_list", foreign_keys=[supervised_id]
    )


class User(CRUD):
    __tablename__ = "user"

    id = Column(String(255), primary_key=True, index=True)
    email = Column(String(255), nullable=False, index=True)
    invitation = Column(String(255), nullable=False, index=True)

    name = Column(String(255), nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    sex = Column(String(255), nullable=True)
    birth = Column(DateTime, nullable=True)
    avatar = Column(String(255), nullable=True)
    phone = Column(Integer, nullable=True)

    disabled = Column(Boolean, nullable=False, default=False)

    def create(self):
        self.invitation = generate_code()
        return super().create()

    def accept_invitation(self, invitation_code):
        supervisor = User(self.db, User.invitation == invitation_code).get()
        if supervisor is None:
            raise translations["errors"]["supervisors"]["code_not_valid"]
        if supervisor.id == self.id:
            raise translations["errors"]["supervisors"]["cannot_be_yourself"]
        already_supervised = (
            Supervised(
                self.db,
                or_(Supervised.supervisor == supervisor, Supervised.supervised == self),
            ).get()
            is not None
        )
        if already_supervised:
            raise translations["errors"]["supervisors"]["already_supervised"]
        supervisor.invitation = generate_code()

        supervisor.save()
        Supervised(self.db, supervisor=supervisor, supervised=self).create()

        message = NewSupervisorMessage(supervisor=supervisor)
        self.send_notification(message)

    @property
    def supervised(self):
        supervised_list = []
        for supervised in self.supervised_list:
            supervised.supervised.db = self.db
            supervised_list.append(supervised.supervised)
        return supervised_list

    @property
    def supervisors(self):
        supervisors_list = []
        for supervisor in self.supervisors_list:
            supervisor.supervisor.db = self.db
            supervisors_list.append(supervisor.supervisor)
        return supervisors_list

    @property
    def notification_preferences(self):
        return [str(preference) for preference in self.notification_preferences_list]

    def send_notification(self, message: Message):
        for notification_preference in self.notification_preferences_list:
            thread = threading.Thread(
                target=notification_preference.send_notification, args=(message,)
            )
            thread.start()
