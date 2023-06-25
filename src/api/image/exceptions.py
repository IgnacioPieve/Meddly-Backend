from fastapi import HTTPException
from starlette import status

from api.exceptions import GenericException

ERROR800 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 800,
        "description": "This image does not exists or you do not have access to it.",
    },
)


class ImageDoesNotExist(GenericException):
    http_exception = ERROR800
