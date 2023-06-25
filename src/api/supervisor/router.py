from fastapi import APIRouter, Depends
from starlette.background import BackgroundTasks

from api.auth.dependencies import authenticate
from api.exceptions import GenericException
from api.supervisor.service import accept_invitation as accept_invitation_service
from api.supervisor.service import delete_supervised as delete_supervised_service
from api.supervisor.service import delete_supervisor as delete_supervisor_service
from api.supervisor.service import get_supervised as get_supervised_service
from api.supervisor.service import get_supervisors as get_supervisors_service
from api.user.models import User
from api.user.schemas import UserSchema

router = APIRouter(prefix="/supervisors", tags=["Supervisors"])


@router.post("/invitation", status_code=200, summary="Accept invitation")
async def accept_invitation(
    code: str,
    background_tasks: BackgroundTasks,
    user: User = Depends(authenticate),
):
    """
    # Accept invitation

    This endpoint allows the authenticated user to accept an invitation.

    Args:
    - **code** (str): The invitation code.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.
    """

    try:
        await accept_invitation_service(user, code, background_tasks)
    except GenericException as e:
        raise e.http_exception


@router.get(
    "/supervisor",
    response_model=list[UserSchema],
    status_code=200,
    summary="Get supervisors",
)
async def get_supervisors(user: User = Depends(authenticate)):
    """
    # Get supervisors

    This endpoint allows the authenticated user to retrieve a list of supervisors.

    Args:
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **List[UserSchema]**: A list of supervisor data.
    """

    supervisors = await get_supervisors_service(user)
    return supervisors


@router.get(
    "/supervised",
    response_model=list[UserSchema],
    status_code=200,
    summary="Get supervised users",
)
async def get_supervised(user: User = Depends(authenticate)):
    """
    # Get supervised users

    This endpoint allows the authenticated user to retrieve a list of supervised users.

    Args:
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **List[UserSchema]**: A list of supervised user data.
    """

    supervised = await get_supervised_service(user)
    return supervised


@router.delete(
    "/supervisor/{supervisor_id}",
    status_code=200,
    summary="Delete supervisor",
)
async def delete_supervisor(supervisor_id: str, user: User = Depends(authenticate)):
    """
    # Delete supervisor

    This endpoint allows the authenticated user to delete a supervisor.

    Args:
    - **supervisor_id** (str): The ID of the supervisor to be deleted.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.
    """

    try:
        await delete_supervisor_service(supervisor_id, user)
    except GenericException as e:
        raise e.http_exception


@router.delete(
    "/supervised/{supervised_id}",
    status_code=200,
    summary="Delete supervised",
)
async def delete_supervised(supervised_id: str, user: User = Depends(authenticate)):
    """
    # Delete supervised

    This endpoint allows the authenticated user to delete a supervised user.

    Args:
    - **supervised_id** (str): The ID of the supervised user to be deleted.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.
    """

    try:
        await delete_supervised_service(supervised_id, user)
    except GenericException as e:
        raise e.http_exception
