from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship

from models import CRUD


class Appointment(CRUD):
    __tablename__ = "appointment"

    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="appointments", foreign_keys=[user_id])

    date = Column(DateTime, nullable=False, index=True)
    name = Column(String(255), nullable=False)

    doctor = Column(String(255), nullable=True)
    speciality = Column(String(255), nullable=True)
    location = Column(String(255), nullable=True)
    notes = Column(String(2048), nullable=True)
