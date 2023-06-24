from fastapi import HTTPException
from starlette import status

from api.exceptions import GenericException

# Medicines has the 3xx errors
ERROR300 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 300,
        "description": "You can not create a medicine with interval and selected days at the same time.",
    },
)
ERROR301 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 301,
        "description": "You must select at least one hour.",
    },
)
ERROR302 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 302,
        "description": "Invalid date.",
    },
)
ERROR303 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 303,
        "description": "Invalid hour (with correct format).",
    },
)
ERROR304 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 304,
        "description": "Incorrect hour format.",
    },
)
ERROR305 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 305,
        "description": "The medicine does not exist or you do not have permission to access it.",
    },
)
ERROR306 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 306,
        "description": "This consumption already exists.",
    },
)
ERROR307 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 307,
        "description": "This consumption does not exist.",
    },
)


class IntervalAndDays(GenericException):
    http_exception = ERROR300


class NoHourSelected(GenericException):
    http_exception = ERROR301


class InvalidDate(GenericException):
    http_exception = ERROR302


class InvalidHour(GenericException):
    http_exception = ERROR303


class IncorrectHourFormat(GenericException):
    http_exception = ERROR304


class MedicineNotFound(GenericException):
    http_exception = ERROR305


class ConsumptionAlreadyExists(GenericException):
    http_exception = ERROR306


class ConsumptionDoesNotExist(GenericException):
    http_exception = ERROR307
