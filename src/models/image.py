import os

from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship, Session

from models.utils import CRUD
from uuid import uuid4
from PIL import Image as PILImage


class Image(CRUD):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(255), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="images", foreign_keys=[user_id])

    def set_image(self, image: PILImage):
        folder = 'store/images'
        file_name = f'{uuid4()}.jpg'
        # Assert that the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = f'{folder}/{file_name}'
        image.save(path)
        self.path = path
