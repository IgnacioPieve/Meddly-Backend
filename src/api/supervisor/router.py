from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate
from api.supervisor.service import accept_invitation as accept_invitation_service
from api.supervisor.service import delete_supervised as delete_supervised_service
from api.supervisor.service import delete_supervisor as delete_supervisor_service
from api.supervisor.service import get_supervised as get_supervised_service
from api.supervisor.service import get_supervisors as get_supervisors_service
from api.user.models import User

router = APIRouter(prefix="/supervisors", tags=["Supervisors"])


@router.post("/invitation", status_code=200, summary="Accept invitation")
async def accept_invitation(code: str, user: User = Depends(authenticate)):
    await accept_invitation_service(user, code)
    return True


@router.get(
    "/supervisor", response_model=list[str], status_code=200, summary="Get supervisors"
)
async def get_supervisors(user: User = Depends(authenticate)):
    supervisors = await get_supervisors_service(user)
    return supervisors


@router.get(
    "/supervised",
    response_model=list[str],
    status_code=200,
    summary="Get supervised users",
)
async def get_supervised(user: User = Depends(authenticate)):
    supervised = await get_supervised_service(user)
    return supervised


@router.delete(
    "/supervisor/{supervisor_id}",
    status_code=200,
    summary="Delete supervisor",
)
async def delete_supervisor(supervisor_id: str, user: User = Depends(authenticate)):
    await delete_supervisor_service(supervisor_id, user)


@router.delete(
    "/supervised/{supervised_id}",
    status_code=200,
    summary="Delete supervised",
)
async def delete_supervised(supervised_id: str, user: User = Depends(authenticate)):
    await delete_supervised_service(supervised_id, user)
