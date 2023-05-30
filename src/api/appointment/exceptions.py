from fastapi import HTTPException
from starlette import status

# Appointments has the 4xx errors
ERROR400 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 400,
        "description": "The appointment does not exist or you do not have permission to access it.",
    },
)
