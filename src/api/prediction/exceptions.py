from fastapi import HTTPException
from starlette import status

ERROR700 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 700,
        "description": "Some of the symptoms are not valid. "
        "Remember that you can only use the symptoms that appear in the list "
        "and you have to send the code, not the name of the symptom.",
    },
)
ERROR701 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 701, "description": "The prediction has been already verified."},
)
ERROR702 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 702,
        "description": "The prediction does not exist or you do not have permission to access it.",
    },
)
ERROR703 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 703,
        "description": "If you want to use pagination, you have to send both page and per_page.",
    },
)
