from sklearn.preprocessing import LabelEncoder
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship
from tensorflow.keras.models import load_model

from api.prediction.exceptions import ERROR701
from api.prediction.models.prediction import Prediction
from models import CRUD

classes = [
    "Actinic keratoses",
    "Basal cell carcinoma",
    "Benign keratosis-like lesions",
    "Dermatofibroma",
    "Melanoma",
    "Melanocytic nevi",
    "Vascular lesions",
]
le = LabelEncoder()
le.fit(classes)
le.inverse_transform([2])

model_trained = load_model("api/prediction/trained/by_image.trained")


class DiseaseImage(CRUD):
    __tablename__ = "verified_disease_image"
    image_name = Column(
        String(255), ForeignKey("image.name"), index=True, nullable=False
    )
    image = relationship("Image", foreign_keys=[image_name])
    predicted_disease = Column(String(255), nullable=False)
    real_disease = Column(String(255), nullable=False)


class PredictionByImage(Prediction):
    __tablename__ = "prediction_by_image"
    image_name = Column(
        String(255), ForeignKey("image.name"), index=True, nullable=False
    )
    image = relationship("Image", foreign_keys=[image_name])
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="predictions_by_image", foreign_keys=[user_id])

    def verify(self, disease: str, approval_to_save: bool = False):
        if self.verified:
            raise ERROR701
        self.image.db = self.db
        if approval_to_save:
            DiseaseImage(
                self.db,
                image=self.image.get_anonymous_copy(tag="DiseaseImage"),
                predicted_disease=self.prediction[0]["disease"],
                real_disease=disease,
            ).create()
        self.verified = True
        self.save()