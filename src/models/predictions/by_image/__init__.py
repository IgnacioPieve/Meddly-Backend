import numpy as np
from fastapi import UploadFile
from PIL import Image
from sklearn.preprocessing import LabelEncoder
from sqlalchemy import Column, Integer, PickleType, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from tensorflow.keras.models import load_model

from models.utils import CRUD

classes = ['Actinic keratoses', 'Basal cell carcinoma', 'Benign keratosis-like lesions',
           'Dermatofibroma', 'Melanoma', 'Melanocytic nevi', 'Vascular lesions']
le = LabelEncoder()
le.fit(classes)
le.inverse_transform([2])

model_trained = load_model("models/predictions/by_image/model.trained")



class PredictionByImage(CRUD):
    __tablename__ = "prediction_by_image"
    id = Column(Integer, primary_key=True, index=True)
    image = Column(Integer, nullable=True)
    prediction = Column(PickleType(), nullable=False)
    user_id = Column(String(255), ForeignKey("user.id"), index=True, nullable=False)
    user = relationship("User", backref="predictions_by_image", foreign_keys=[user_id])
    verified = Column(Boolean, default=False)

    def predict(self, file: UploadFile):
        img = np.asarray(Image.open(file.file).resize((32, 32)))
        img = img / 255.  # Scale pixel values
        img = np.expand_dims(img, axis=0)  # Get it tready as input to the network

        prediction = model_trained.predict(img)
        prediction = [{"disease": classes[i], "probability": prediction[0][i]} for i in np.argsort(prediction[0])[::-1]]

        self.prediction = prediction
        self.create()
        return prediction



