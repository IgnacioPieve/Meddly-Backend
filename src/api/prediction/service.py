import json
import os
from datetime import datetime
from uuid import uuid4

import numpy as np
import pandas as pd
from fastapi import UploadFile
from PIL import Image
from sqlalchemy import insert, select, update

from api.image.models import Image as ImageModel
from api.image.service import save_image, anonymous_copy_image
from api.prediction.exceptions import ERROR703, ERROR700, ERROR701, ERROR702
from api.prediction.models.by_image import PredictionByImage, DiseaseImage
from api.prediction.models.by_image import model_trained as model_trained_by_image
from api.prediction.models.by_symptom import PredictionBySymptom, DiseaseSymptoms
from api.prediction.models.by_symptom import model_trained as model_trained_by_symptom
from api.prediction.models.by_symptom import symptoms, symptoms_template
from api.user.models import User
from database import database

file = "api/search/indexes/codes_translated.json"
with open(file, "r", encoding="utf-8") as f:
    codes = json.load(f)


async def predict_by_symptoms(symptoms_typed: list[str], user: User):
    for symptom in symptoms_typed:
        if symptom not in symptoms:
            raise ERROR700

    symptoms_df = pd.DataFrame(
        [{**symptoms_template, **{symptom: 1 for symptom in symptoms_typed}}]
    )
    symptoms_df = symptoms_df.reindex(columns=symptoms)
    probabilities = model_trained_by_symptom.predict_proba(symptoms_df)

    n = 5
    predictions = np.argsort(probabilities[0])[-n:][::-1]
    results = [
        {
            "disease": model_trained_by_symptom.classes_[predictions][i],
            "probability": probabilities[0][predictions[i]],
        }
        for i in range(len(predictions))
    ]

    insert_query = insert(PredictionBySymptom).values(
        user_id=user.id,
        symptoms=symptoms_typed,
        prediction=results,
    )
    await database.execute(query=insert_query)

    for i in range(len(results)):
        results[i]["disease"] = codes[results[i]["disease"]]
    return results


async def get_predictions_by_symptoms(
    user: User, start: datetime = None, page: int = None, per_page: int = None
):
    select_query = (
        select(PredictionBySymptom)
        .where(PredictionBySymptom.user_id == user.id)
        .order_by(PredictionBySymptom.created_at.desc())
    )
    if start:
        select_query = select_query.where(PredictionBySymptom.created_at >= start)
    if page and per_page:
        select_query = select_query.limit(per_page).offset((page - 1) * per_page)
    if (page or per_page) and not (page and per_page):
        raise ERROR703

    results = await database.fetch_all(query=select_query)
    for result in results:
        result.prediction = json.loads(result.prediction)
        for i in range(len(result.prediction)):
            result.prediction[i]["disease"] = codes[result.prediction[i]["disease"]]
    return results

async def verify_prediction_by_symptom(
    user: User,
    prediction_id: int,
    real_disease: str,
    approval_to_save: bool = False,
) -> bool:
    select_query = select(PredictionBySymptom).where(
        PredictionBySymptom.user_id == user.id,
        PredictionBySymptom.id == prediction_id,
    )
    prediction: PredictionBySymptom = await database.fetch_one(query=select_query)

    if not prediction:
        raise ERROR702
    if prediction.verified:
        raise ERROR701

    if approval_to_save:
        insert_query = insert(DiseaseSymptoms).values(
            symptoms=prediction.symptoms,
            predicted_disease=json.loads(prediction.prediction)[0]["disease"],
            real_disease=real_disease,
        )
        await database.execute(query=insert_query)

    update_query = (
        update(PredictionBySymptom)
        .where(PredictionBySymptom.id == prediction_id)
        .values(
            verified=True,
            real_disease=real_disease,
        )
    )
    await database.execute(query=update_query)

    return True




async def predict_by_image(file: UploadFile, user: User):
    def _predict():
        img = np.asarray(Image.open(file.file).resize((32, 32)))
        img = img / 255.0  # Scale pixel values
        img = np.expand_dims(img, axis=0)  # Get it tready as input to the network

        prediction = model_trained_by_image.predict(img)
        return [
            {"disease": classes[i], "probability": round(float(prediction[0][i]), 2)}
            for i in np.argsort(prediction[0])[::-1]
        ]

    classes = [
        "Queratosis actínica",
        "Carcinoma de células basales",
        "Lesiones benignas similares a queratosis",
        "Dermatofibroma",
        "Melanoma",
        "Nevus melanocíticos",
        "Lesiones vasculares",
    ]

    file_name = await save_image(file.file, user=user, tag='prediction_by_image')
    prediction = _predict()

    insert_query = insert(PredictionByImage).values(
        image_name=file_name,
        user_id=user.id,
        prediction=prediction,
    )
    await database.execute(query=insert_query)

    return prediction


async def get_predictions_by_image(
    user: User, start: datetime = None, page: int = None, per_page: int = None
):
    select_query = (
        select(PredictionByImage)
        .where(PredictionByImage.user_id == user.id)
        .order_by(PredictionByImage.created_at.desc())
    )
    if start:
        select_query = select_query.where(PredictionByImage.created_at >= start)
    if page and per_page:
        select_query = select_query.limit(per_page).offset((page - 1) * per_page)
    if (page or per_page) and not (page and per_page):
        raise ERROR703
    select_query = select_query.order_by(PredictionByImage.created_at.desc())
    results = await database.fetch_all(query=select_query)
    for result in results:
        result.prediction = json.loads(result.prediction)
    return results

async def verify_prediction_by_image(
    user: User,
    prediction_id: int,
    real_disease: str,
    approval_to_save: bool = False,
) -> bool:
    select_query = select(PredictionByImage).where(
        PredictionByImage.user_id == user.id,
        PredictionByImage.id == prediction_id,
    )
    prediction: PredictionByImage = await database.fetch_one(query=select_query)

    if not prediction:
        raise ERROR702
    if prediction.verified:
        raise ERROR701

    if approval_to_save:
        file_name = await anonymous_copy_image(prediction.image_name, tag='prediction_by_image')
        insert_query = insert(DiseaseImage).values(
            image_name=file_name,
            predicted_disease=json.loads(prediction.prediction)[0]["disease"],
            real_disease=real_disease
        )
        await database.execute(query=insert_query)

    update_query = (
        update(PredictionByImage)
        .where(PredictionByImage.id == prediction_id)
        .values(
            verified=True,
            real_disease=real_disease,
        )
    )
    await database.execute(query=update_query)

    return True




