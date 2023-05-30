from fastapi import HTTPException
from starlette import status

# Measurements has the 6xx errors
ERROR600 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 600,
        "description": "The measurement does not exist or you do not have permission to access it.",
    },
)
