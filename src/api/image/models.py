import os
from uuid import uuid4

from PIL import Image as PILImage
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

    def set_image(self, image: PILImage):
        folder = "store/images"
        file_name = f"{uuid4()}.jpg"
        # Assert that the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)
        image.save(f"{folder}/{file_name}")
        self.name = file_name

    def get_anonymous_copy(self, tag: str = None):
        folder = "store/images"
        file_name = f"{uuid4()}.jpg"
        # Assert that the folder exists
        if not os.path.exists(folder):
            os.makedirs(folder)
        PILImage.open(f"{folder}/{self.name}").save(f"{folder}/{file_name}")
        image = Image(self.db)
        image.name = file_name
        image.tag = tag if tag else self.tag
        image.create()
        return image
