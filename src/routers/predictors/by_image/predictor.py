import numpy as np
from fastapi import UploadFile
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import load_model

classes = ['Actinic keratoses', 'Basal cell carcinoma',
           'Benign keratosis-like lesions', 'Dermatofibroma', 'Melanoma',
           'Melanocytic nevi', 'Vascular lesions']
le = LabelEncoder()
le.fit(classes)
le.inverse_transform([2])

model_trained = load_model("routers/predictors/by_image/model.trained")


def predict(file: UploadFile):
    img = np.asarray(Image.open(file.file).resize((32, 32)))

    img = img / 255.  # Scale pixel values

    img = np.expand_dims(img, axis=0)  # Get it tready as input to the network

    pred = model_trained.predict(img)  # Predict
    return [{"disease": classes[i], "probability": pred[0][i]} for i in np.argsort(pred[0])[::-1]]
