import numpy as np
import pandas as pd
import whoosh.index as index
from joblib import load
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import Boolean, Column, ForeignKey, Integer, PickleType, String
from sqlalchemy.orm import relationship
from whoosh.qparser import QueryParser

from models.utils import CRUD, raise_errorcode

model_trained: DecisionTreeClassifier = load(
    "models/predictions/by_symptom/model.trained"
)

symptoms = model_trained.feature_names_in_
symptoms_template = {symptom: 0 for symptom in symptoms}
diseases = model_trained.classes_

code_index = index.open_dir("indexes/symptoms_index")
searcher = {"es": code_index.searcher()}
query_parser = {"es": QueryParser("description", schema=code_index.schema)}


class DiseaseSymptoms(CRUD):
    __tablename__ = "verified_disease_symptoms"
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
    user = relationship(
        "User", backref="predictions_by_symptoms", foreign_keys=[user_id]
    )
    verified = Column(Boolean, default=False)

    def predict(self, symptoms_typed: list[str]):
        for symptom in symptoms_typed:
            if symptom not in symptoms:
                raise_errorcode(700)

        symptoms_df = pd.DataFrame(
            [{**symptoms_template, **{symptom: 1 for symptom in symptoms_typed}}]
        )
        symptoms_df = symptoms_df.reindex(columns=symptoms)
        probabilities = model_trained.predict_proba(symptoms_df)

        n = 5
        predictions = np.argsort(probabilities[0])[-n:][::-1]
        results = [
            {
                "disease": model_trained.classes_[predictions][i],
                "probability": probabilities[0][predictions[i]],
            }
            for i in range(len(predictions))
        ]

        self.symptoms = symptoms_typed
        self.prediction = results
        self.create()
        return results

    @staticmethod
    def search(symptom_typed: str, language: str):
        results = searcher[language].search(
            query_parser[language].parse(f"{symptom_typed.strip()}*")
        )
        return [
            {"code": result["code"], "description": result["description"]}
            for result in results
        ]

    def verify(self, disease: str):
        if self.verified:
            raise_errorcode(701)
        DiseaseSymptoms(
            self.db,
            symptoms=self.symptoms,
            predicted_disease=self.prediction[0]["disease"],
            real_disease=disease,
        ).create()
        self.verified = True
        self.save()
