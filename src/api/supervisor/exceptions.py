from fastapi import HTTPException
from starlette import status

from api.exceptions import GenericException

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
ERROR205 = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={
        "code": 205,
        "description": "Some of the selected users are not supervised by you or do not exist.",
    },
)


class UserIsAlreadySupervisor(GenericException):
    http_exception = ERROR200


class InvalidInvitationCode(GenericException):
    http_exception = ERROR201


class SupervisorNotFound(GenericException):
    http_exception = ERROR202


class SupervisedNotFound(GenericException):
    http_exception = ERROR203


class UserIsSupervisingHimself(GenericException):
    http_exception = ERROR204
