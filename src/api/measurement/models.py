from sqlalchemy import Column, DateTime, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from models import CRUD


class Measurement(CRUD):
    __tablename__ = "measurement"

    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="measurements", foreign_keys=[user_id])

    date = Column(DateTime, nullable=False, index=True)
    type = Column(String(255), nullable=False)
    value = Column(Float, nullable=False)
    unit = Column(String(255), nullable=False)
