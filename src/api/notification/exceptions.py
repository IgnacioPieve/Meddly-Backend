from fastapi import HTTPException
from starlette import status

ERROR500 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 500,
        "description": "You tried to add a notification preference that you already have.",
    },
)
ERROR501 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 501,
        "description": "You tried to delete a notification preference that you don't have.",
    },
)
