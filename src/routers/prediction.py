import pickle

import numpy as np
import pandas as pd
from fastapi import APIRouter, Depends
from joblib import load
from sklearn.tree import DecisionTreeClassifier
from sqlalchemy import and_, exc

from dependencies import auth
from models.notification import NotificationPreference
from models.utils import raise_errorcode
from schemas.utils import SearchResultSchema

router = APIRouter(prefix="/prediction", tags=["Predictions"])

model_trained: DecisionTreeClassifier = load("routers/prediction_files/model.trained")
with open("routers/prediction_files/symptoms.pickle", "rb") as f:
    symptoms = model_trained.feature_names_in_
    symptoms_template = {symptom: 0 for symptom in symptoms}


@router.post(
    "symptom",
    response_model=SearchResultSchema,
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "symptom/",
    response_model=SearchResultSchema,
    status_code=200,
    summary="symptom_search",
)
def symptom_search(symptom: str, authentication=Depends(auth.authenticate)):
    """
    symptom_search
    """
    _, _ = authentication
    symptom_typed = symptom
    results = []
    for symptom in symptoms:
        if symptom_typed in symptom:
            results.append(symptom)
            if len(results) > 10:
                return {"results": results}
    return {"results": results}


@router.post(
    "symptom/prediction",
    response_model=SearchResultSchema,
    status_code=200,
    include_in_schema=False,
)
@router.post(
    "symptom/prediction/",
    response_model=SearchResultSchema,
    status_code=200,
    summary="symptom_prediction",
)
def symptom_prediction(
    symptoms_typed: list[str], authentication=Depends(auth.authenticate)
):
    _, _ = authentication
    for symptom in symptoms_typed:
        if symptom not in symptoms:
            raise_errorcode(700)
    symptoms_typed = {symptom: 1 for symptom in symptoms_typed}
    symptoms_typed = {**symptoms_template, **symptoms_typed}
    symptoms_typed = pd.DataFrame([symptoms_typed])
    symptoms_typed = symptoms_typed.reindex(columns=symptoms)
    print(symptoms_typed)
    prediction = model_trained.predict(symptoms_typed)[0]
    print(model_trained.predict(symptoms_typed))
    print(model_trained.predict_proba(symptoms_typed))

    return {"results": [str(prediction)]}
