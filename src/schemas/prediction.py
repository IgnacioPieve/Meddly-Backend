import datetime

from pydantic import BaseModel


class ProbabilitySchema(BaseModel):
    disease: str
    probability: float

class PredictionSchema(BaseModel):
    id: int
    created_at: datetime.datetime
    prediction: list[ProbabilitySchema]
    verified: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "prediction": [
                    {
                        "disease": "COVID-19",
                        "probability": 0.9
                    },
                    {
                        "disease": "Gripe",
                        "probability": 0.1
                    }
                ],
                "verified": False
            }
        }

class PredictionByImageSchema(PredictionSchema):
    image_name: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                **PredictionSchema.Config.schema_extra["example"],
                "image_name": "https://local:11001/0Z9O9ZP.png"
            }
        }

class PredictionBySymptomSchema(PredictionSchema):
    symptoms: list[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                **PredictionSchema.Config.schema_extra["example"],
                "symptoms": ["Fiebre", "Tos"]
            }
        }