from fastapi import HTTPException
from starlette import status

ERROR203 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 203,
        "description": "Supervisor not found.",
    },
)
