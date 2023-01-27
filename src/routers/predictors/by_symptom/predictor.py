import numpy as np
import pandas as pd
from joblib import load
from sklearn.tree import DecisionTreeClassifier

model_trained: DecisionTreeClassifier = load("routers/predictors/by_symptom/model.trained")
symptoms = model_trained.feature_names_in_
symptoms_template = {symptom: 0 for symptom in symptoms}


def predict(symptoms_typed: list[str]):
    symptoms_typed = {symptom: 1 for symptom in symptoms_typed}
    symptoms_typed = {**symptoms_template, **symptoms_typed}
    symptoms_typed = pd.DataFrame([symptoms_typed])
    symptoms_typed = symptoms_typed.reindex(columns=symptoms)
    probabilities = model_trained.predict_proba(symptoms_typed)

    results = []
    n = 5
    predictions = np.argsort(probabilities[0])[-n:][::-1]
    predictions_names = model_trained.classes_[predictions]
    for i in range(len(predictions)):
        results.append({
            'disease': predictions_names[i],
            'probability': probabilities[0][predictions[i]]
        })

    return results

def search(symptom_typed: str):
    results = []
    for symptom in symptoms:
        if symptom_typed in symptom:
            results.append(symptom)
            if len(results) > 10:
                return {"results": results}
    return {"results": results}