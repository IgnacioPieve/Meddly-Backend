from fastapi import APIRouter, Depends, UploadFile
from PIL import Image
from starlette.responses import Response

from dependencies import auth
from models.image import Image as ImageModel
from models.predictions.by_image import PredictionByImage
from models.predictions.by_symptom import PredictionBySymptom
from schemas.prediction import ProbabilitySchema
from schemas.utils import SearchResultSchema

router = APIRouter(prefix="/image", tags=["Images"])


@router.get(
    "/{name}",
    responses={
        200: {
            "content": {"image/jpg": {}}
        }
    },
    response_class=Response,
    include_in_schema=False,
)
@router.get(
    "/{name}/",
    responses={
        200: {
            "content": {"image/jpg": {}}
        }
    },
    response_class=Response,
    summary="Get an image",
)
def get_image(name: str, authentication=Depends(auth.authenticate)):
    user, db = authentication
    image = ImageModel(db, ImageModel.user_id==user.id, ImageModel.name==name).get()
    return Response(content=image.get_bytes(), media_type="image/jpg")