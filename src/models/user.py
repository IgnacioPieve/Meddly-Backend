from sqlalchemy import Column, String, DateTime, Float, Integer, ForeignKey, or_
from sqlalchemy.orm import  relationship

from models.utils import CRUD, generate_code
from config import translations


class Supervised(CRUD):
    __tablename__ = 'supervised'
    id = Column(Integer, primary_key=True, index=True)
    supervisor_id = Column(String, ForeignKey('user.id'), nullable=False, index=True)
    supervisor = relationship('User', backref='supervised_list', foreign_keys=[supervisor_id])
    supervised_id = Column(String, ForeignKey('user.id'), nullable=False, index=True)
    supervised = relationship('User', backref='supervisors_list', foreign_keys=[supervised_id])


class User(CRUD):
    __tablename__ = "user"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    invitation = Column(String, nullable=False, index=True)

    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    sex = Column(String, nullable=True)
    birth = Column(DateTime, nullable=True)
    avatar = Column(String, nullable=True)

    def create(self):
        self.invitation = self.generate_code()
        return super().create()

    def accept_invitation(self, invitation_code):
        supervisor = User(self.db, User.invitation == invitation_code).get()
        if supervisor is None:
            raise translations['errors']['supervisors']['code_not_valid']
        already_supervised = Supervised(self.db, or_(Supervised.supervisor == supervisor,
                                                     Supervised.supervised == self)).get() is not None
        if already_supervised:
            raise translations['errors']['supervisors']['already_supervised']
        supervisor.invitation = generate_code()

        supervisor.save()
        Supervised(self.db, supervisor=supervisor, supervised=self).create()

    @property
    def supervised(self):
        supervised_list = []
        for supervised in Supervised(self.db, Supervised.supervisor == self).get_all():
            supervised.supervised.db = self.db
            supervised_list.append(supervised.supervised)
        return supervised_list

    @property
    def supervisors(self):
        supervisors_list = []
        for supervisor in Supervised(self.db, Supervised.supervised == self).get_all():
            supervisor.supervisor.db = self.db
            supervisors_list.append(supervisor.supervisor)
        return supervisors_list
