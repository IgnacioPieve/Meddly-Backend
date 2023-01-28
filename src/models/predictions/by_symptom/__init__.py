import numpy as np
import pandas as pd
from joblib import load
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import Boolean, Column, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship

from models.user import User
from models.utils import CRUD, raise_errorcode

model_trained: DecisionTreeClassifier = load("models/predictions/by_symptom/model.trained")

symptoms = model_trained.feature_names_in_
symptoms_template = {symptom: 0 for symptom in symptoms}
diseases = model_trained.classes_


class DiseaseSymptoms(CRUD):
    __tablename__ = "disease_symptoms"
    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(PickleType(), nullable=False)
    predicted_disease = Column(String(255), nullable=False)
    real_disease = Column(String(255), nullable=False)


class PredictionBySymptom(CRUD):
    __tablename__ = "prediction_by_symptom"
    id = Column(Integer, primary_key=True, index=True)
    symptoms = Column(PickleType(), nullable=False)
    prediction = Column(PickleType(), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="predictions_by_symptoms", foreign_keys=[user_id])
    verified = Column(Boolean, default=False)

    def predict(self, symptoms_typed: list[str]):
        for symptom in symptoms_typed:
            if symptom not in symptoms:
                raise_errorcode(700)

        symptoms_df = pd.DataFrame([{**symptoms_template, **{symptom: 1 for symptom in symptoms_typed}}])
        symptoms_df = symptoms_df.reindex(columns=symptoms)
        probabilities = model_trained.predict_proba(symptoms_df)

        n = 5
        predictions = np.argsort(probabilities[0])[-n:][::-1]
        results = [{'disease': model_trained.classes_[predictions][i], 'probability': probabilities[0][predictions[i]]}
                   for i in range(len(predictions))]

        self.symptoms = symptoms_typed
        self.prediction = results
        self.create()
        return results

    @staticmethod
    def search(symptom_typed: str):
        results = []
        for symptom in symptoms:
            if symptom_typed in symptom:
                results.append(symptom)
                if len(results) > 10:
                    return {"results": results}
        return {"results": results}

    def load_real_disease(self, disease: str):
        if self.verified:
            raise_errorcode(701)
        DiseaseSymptoms(self.db, symptoms=self.symptoms,
                        predicted_disease=self.prediction[0]['disease'], real_disease=disease).create()
        self.verified = True
        self.save()
