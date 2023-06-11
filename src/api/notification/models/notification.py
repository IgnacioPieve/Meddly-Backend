from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import CRUD


class Notification(CRUD):
    __tablename__ = "notification"

    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="notifications_list", foreign_keys=[user_id])
    title = Column(String(255), nullable=False)
    body = Column(String(255), nullable=False)
