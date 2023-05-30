import json
import os
from uuid import uuid4

import numpy as np
import pandas as pd
from fastapi import UploadFile
from PIL import Image
from sqlalchemy import insert, select

from api.image.models import Image as ImageModel
from api.prediction.models.by_image import PredictionByImage
from api.prediction.models.by_image import model_trained as model_trained_by_image
from api.prediction.models.by_symptom import PredictionBySymptom
from api.prediction.models.by_symptom import model_trained as model_trained_by_symptom
from api.prediction.models.by_symptom import symptoms, symptoms_template
from api.user.models import User
from database import database

file = 'api/search/indexes/codes_translated.json'
with open(file, 'r', encoding='utf-8') as f:
    codes = json.load(f)


async def predict_by_symptoms(symptoms_typed: list[str], user: User):
    for symptom in symptoms_typed:
        if symptom not in symptoms:
            raise Exception(700)
            # TODO: raise error

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
        results[i]['disease'] = codes[results[i]['disease']]
    return results


async def get_predictions_by_symptoms(user: User):
    select_query = select(PredictionBySymptom).where(
        PredictionBySymptom.user_id == user.id
    )
    results = await database.fetch_all(query=select_query)
    for result in results:
        result.prediction = json.loads(result.prediction)
        for i in range(len(result.prediction)):
            result.prediction[i]['disease'] = codes[result.prediction[i]['disease']]
    return results


async def predict_by_image(file: UploadFile, user: User):
    classes = [
        "Queratosis actínica",
        "Carcinoma de células basales",
        "Lesiones benignas similares a queratosis",
        "Dermatofibroma",
        "Melanoma",
        "Nevus melanocíticos",
        "Lesiones vasculares",
    ]

    image = Image.open(file.file).resize((512, 512))
    folder = "store/images"
    file_name = f"{uuid4()}.jpg"

    if not os.path.exists(folder):
        os.makedirs(folder)
    image.save(f"{folder}/{file_name}")

    insert_query = insert(ImageModel).values(
        user_id=user.id,
        tag="prediction_by_image",
        name=file_name,
    )
    await database.execute(query=insert_query)

    img = np.asarray(Image.open(file.file).resize((32, 32)))
    img = img / 255.0  # Scale pixel values
    img = np.expand_dims(img, axis=0)  # Get it tready as input to the network

    prediction = model_trained_by_image.predict(img)
    prediction = [
        {"disease": classes[i], "probability": float(prediction[0][i])}
        for i in np.argsort(prediction[0])[::-1]
    ]

    insert_query = insert(PredictionByImage).values(
        image_name=file_name,
        user_id=user.id,
        prediction=prediction,
    )
    await database.execute(query=insert_query)

    return prediction


async def get_predictions_by_image(user: User):
    select_query = select(PredictionByImage).where(PredictionByImage.user_id == user.id)
    results = await database.fetch_all(query=select_query)
    for result in results:
        result.prediction = json.loads(result.prediction)
    return results
