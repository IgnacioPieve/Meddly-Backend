from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from models import CRUD


class Image(CRUD):
    __tablename__ = "image"
    id = None
    name = Column(String(255), primary_key=True, index=True)
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=True)
    user = relationship("User", backref="images", foreign_keys=[user_id])
    tag = Column(String(255), nullable=False)
