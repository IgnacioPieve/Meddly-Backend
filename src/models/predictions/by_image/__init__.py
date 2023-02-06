import numpy as np
from fastapi import UploadFile
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import Boolean, Column, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship
from tensorflow.keras.models import load_model

from models.utils import CRUD, raise_errorcode

classes = [
    "Actinic keratoses",
    "Basal cell carcinoma",
    "Benign keratosis-like lesions",
    "Dermatofibroma",
    "Melanoma",
    "Melanocytic nevi",
    "Vascular lesions",
]
classes = [
    "Actinic keratoses",
    "Cancer bro",
    "No es cancer bro",
    "Dermatofibroma",
    "Melanoma",
    "Melanocytic nevi",
    "Vascular lesions",
]
le = LabelEncoder()
le.fit(classes)
le.inverse_transform([2])

model_trained = load_model("models/predictions/by_image/model.trained")


class DiseaseImage(CRUD):
    __tablename__ = "verified_disease_image"
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(
        String(255), ForeignKey("image.name"), index=True, nullable=False
    )
    image = relationship("Image", foreign_keys=[image_name])
    predicted_disease = Column(String(255), nullable=False)
    real_disease = Column(String(255), nullable=False)


class PredictionByImage(CRUD):
    __tablename__ = "prediction_by_image"
    id = Column(Integer, primary_key=True, index=True)
    image_name = Column(
        String(255), ForeignKey("image.name"), index=True, nullable=False
    )
    image = relationship("Image", foreign_keys=[image_name])
    prediction = Column(PickleType(), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="predictions_by_image", foreign_keys=[user_id])
    verified = Column(Boolean, default=False)

    def predict(self, file: UploadFile):
        img = np.asarray(Image.open(file.file).resize((32, 32)))
        img = img / 255.0  # Scale pixel values
        img = np.expand_dims(img, axis=0)  # Get it tready as input to the network

        prediction = model_trained.predict(img)
        prediction = [
            {"disease": classes[i], "probability": prediction[0][i]}
            for i in np.argsort(prediction[0])[::-1]
        ]

        self.prediction = prediction
        self.create()
        return prediction

    def verify(self, disease: str):
        if self.verified:
            raise_errorcode(701)
        self.image.db = self.db
        DiseaseImage(
            self.db,
            image=self.image.get_anonymous_copy(tag="DiseaseImage"),
            predicted_disease=self.prediction[0]["disease"],
            real_disease=disease,
        ).create()
        self.verified = True
        self.save()
