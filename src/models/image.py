import os
from uuid import uuid4

from PIL import Image as PILImage
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, relationship

from models.utils import CRUD


class Image(CRUD):
    __tablename__ = "image"
    name = Column(String(255), primary_key=True, index=True)
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
        self.name = file_name

    def get_bytes(self):
        folder = 'store/images'
        path = f'{folder}/{self.name}'
        with open(path, 'rb') as file:
            return file.read()
