from fastapi import HTTPException
from starlette import status


class GenericException(Exception):
    http_exception = HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": 0,
            "description": "Generic exception.",
        },
    )
