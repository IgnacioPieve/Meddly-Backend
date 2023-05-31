from fastapi import HTTPException
from starlette import status

ERROR200 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 200, "description": "This user is already your supervisor."},
)
ERROR201 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 201, "description": "Invalid invitation code."},
)
ERROR202 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 202, "description": "Supervisor not found."},
)
ERROR203 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 203, "description": "Supervised not found."},
)
ERROR204 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 204, "description": "You can't supervise yourself."},
)
