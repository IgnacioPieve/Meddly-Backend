from fastapi import HTTPException
from starlette import status

from api.exceptions import GenericException

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
ERROR502 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 502,
        "description": "You tried to add a notification preference that is not in the list of available preferences.",
    },
)
ERROR503 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 503,
        "description": "You tried to delete a notification that does not exist or is not yours.",
    },
)


class YouAlreadyHaveThisNotificationPreference(GenericException):
    http_exception = ERROR500

class YouDontHaveThisNotificationPreference(GenericException):
    http_exception = ERROR501

class ThisNotificationPreferenceDoesNotExist(GenericException):
    http_exception = ERROR502

class ThisNotificationDoesNotExist(GenericException):
    http_exception = ERROR503