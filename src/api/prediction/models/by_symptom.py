from joblib import load
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from api.prediction.exceptions import ERROR701
from api.prediction.models.prediction import Prediction
from models import CRUD

model_trained: DecisionTreeClassifier = load(
    "api/prediction/trained/by_symptom.trained"
)

symptoms = model_trained.feature_names_in_
symptoms_template = {symptom: 0 for symptom in symptoms}
diseases = model_trained.classes_


class DiseaseSymptoms(CRUD):
    __tablename__ = "verified_disease_symptoms"
    symptoms = Column(ARRAY(String), nullable=False)
    predicted_disease = Column(String(255), nullable=False)
    real_disease = Column(String(255), nullable=False)


class PredictionBySymptom(Prediction):
    __tablename__ = "prediction_by_symptom"
    symptoms = Column(ARRAY(String), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship(
        "User", backref="predictions_by_symptoms", foreign_keys=[user_id]
    )

    def verify(self, disease: str, approval_to_save: bool = False):
        if self.verified:
            raise ERROR701
        if approval_to_save:
            DiseaseSymptoms(
                self.db,
                symptoms=self.symptoms,
                predicted_disease=self.prediction[0]["disease"],
                real_disease=disease,
            ).create()
        self.verified = True
        self.save()
