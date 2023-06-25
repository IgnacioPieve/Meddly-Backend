import json
from datetime import datetime

import numpy as np
import pandas as pd
from fastapi import UploadFile
from PIL import Image
from sqlalchemy import insert, select, update

from api.image.service import anonymous_copy_image, save_image
from api.prediction.exceptions import ERROR700, ERROR701, ERROR702
from api.prediction.models.by_image import DiseaseImage, PredictionByImage
from api.prediction.models.by_image import model_trained as model_trained_by_image
from api.prediction.models.by_symptom import DiseaseSymptoms, PredictionBySymptom
from api.prediction.models.by_symptom import model_trained as model_trained_by_symptom
from api.prediction.models.by_symptom import symptoms, symptoms_template
from api.user.models import User
from database import database

file = "api/search/indexes/codes_translated.json"
with open(file, "r", encoding="utf-8") as f:
    codes = json.load(f)


async def predict_by_symptoms(symptoms_typed: list[str], user: User) -> list[dict]:
    """
    Predicts diseases based on typed symptoms.

    Args:
        symptoms_typed (list[str]): A list of symptoms typed by the user.
        user (User): An instance of the User class representing the user.

    Returns:
        list[dict]: A list of dictionaries containing disease predictions and their probabilities.
    """

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
    """
    Retrieves predictions of diseases based on symptoms for a specific user.

    Args:
        user (User): An instance of the User class representing the user.
        start (datetime, optional): The start datetime to filter the predictions. Defaults to None.
        page (int, optional): The page number for pagination. Defaults to None.
        per_page (int, optional): The number of results per page for pagination. Defaults to None.
    """

    select_query = (
        select(PredictionBySymptom)
        .where(PredictionBySymptom.user_id == user.id)
        .order_by(PredictionBySymptom.created_at.desc())
    )
    if start:
        select_query = select_query.where(PredictionBySymptom.created_at >= start)
    if page and per_page:
        select_query = select_query.limit(per_page).offset((page - 1) * per_page)

    results = await database.fetch_all(query=select_query)
    for result in results:
        result.symptoms = [
            {"code": symptom, "description": codes[symptom]}
            for symptom in result.symptoms
        ]
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
    """
    Verifies a prediction by symptom for a user.

    Args:
        user (User): An instance of the User class representing the user.
        prediction_id (int): The ID of the prediction to verify.
        real_disease (str): The actual disease associated with the symptoms.
        approval_to_save (bool, optional): Flag indicating whether the user consents to anonymously use their diagnosis for further retraining of the AI model.
                                            Defaults to False, indicating that the user does not provide consent to save their diagnosis for retraining.
    """

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


async def predict_by_image(file: UploadFile, user: User) -> list[dict]:
    """
    Predicts diseases based on an image.

    Args:
        file (UploadFile): An instance of the UploadFile class representing the image file.
        user (User): An instance of the User class representing the user.

    Returns:
        list[dict]: A list of dictionaries containing disease predictions and their probabilities.
    """

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

    file_name = await save_image(file.file, user=user, tag="prediction_by_image")
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
    """
    Retrieves predictions of diseases based on images for a specific user.

    Args:
        user (User): An instance of the User class representing the user.
        start (datetime, optional): The start datetime to filter the predictions. Defaults to None.
        page (int, optional): The page number for pagination. Defaults to None.
        per_page (int, optional): The number of results per page for pagination. Defaults to None.
    """

    select_query = (
        select(PredictionByImage)
        .where(PredictionByImage.user_id == user.id)
        .order_by(PredictionByImage.created_at.desc())
    )
    if start:
        select_query = select_query.where(PredictionByImage.created_at >= start)
    if page and per_page:
        select_query = select_query.limit(per_page).offset((page - 1) * per_page)

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
    """
    Verifies a prediction by image for a user.

    Args:
        user (User): An instance of the User class representing the user.
        prediction_id (int): The ID of the prediction to verify.
        real_disease (str): The actual disease associated with the image.
        approval_to_save (bool, optional): Flag indicating whether the user consents to anonymously use their diagnosis for further retraining of the AI model.
                                            Defaults to False, indicating that the user does not provide consent to save their diagnosis for retraining.
    """

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
        file_name = await anonymous_copy_image(
            prediction.image_name, tag="prediction_by_image"
        )
        insert_query = insert(DiseaseImage).values(
            image_name=file_name,
            predicted_disease=json.loads(prediction.prediction)[0]["disease"],
            real_disease=real_disease,
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
