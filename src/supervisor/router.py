from fastapi import APIRouter, Depends
from sqlalchemy import and_

from auth.dependencies import authenticate
from models import raise_errorcode
from user.models import Supervised

router = APIRouter(prefix="/supervisors", tags=["Supervisors"])


@router.post("/invitation", status_code=200, include_in_schema=False)
@router.post("/invitation/", status_code=200, summary="Accept invitation")
def accept_invitation(code: str, authentication=Depends(authenticate)):
    """
    Acepta un código de invitación
    """
    user, _ = authentication
    user.accept_invitation(code)


@router.get(
    "/supervisor", response_model=list[str], status_code=200, include_in_schema=False
)
@router.get(
    "/supervisor/", response_model=list[str], status_code=200, summary="Get supervisors"
)
def get_supervisors(authentication=Depends(authenticate)):
    """
    Obtiene la lista de supervisores
    """
    user, _ = authentication
    return [supervisor.supervisor.id for supervisor in user.supervisors_list]


@router.get(
    "/supervised", response_model=list[str], status_code=200, include_in_schema=False
)
@router.get(
    "/supervised/",
    response_model=list[str],
    status_code=200,
    summary="Get supervised users",
)
def get_supervised(authentication=Depends(authenticate)):
    """
    Obtiene la lista de usuarios supervisados
    """
    user, _ = authentication
    return [supervised.supervised.id for supervised in user.supervised_list]


@router.delete(
    "/supervisor/{supervisor_id}",
    status_code=200,
    include_in_schema=False,
)
@router.delete(
    "/supervisor/{supervisor_id}/",
    status_code=200,
    summary="Delete supervisor",
)
def delete_supervisor(supervisor_id: str, authentication=Depends(authenticate)):
    """
    Elimina un supervisor
    """
    user, db = authentication
    supervisor = Supervised(
        db,
        and_(Supervised.supervisor_id == supervisor_id, Supervised.supervised == user),
    ).get()
    if supervisor is None:
        raise_errorcode(202)
    supervisor.destroy()


@router.delete(
    "/supervised/{supervised_id}",
    status_code=200,
    include_in_schema=False,
)
@router.delete(
    "/supervised/{supervised_id}/",
    status_code=200,
    summary="Delete supervised",
)
def delete_supervised(supervised_id: str, authentication=Depends(authenticate)):
    """
    Elimina un supervisado
    """
    user, db = authentication
    supervised = Supervised(
        db,
        and_(Supervised.supervisor == user, Supervised.supervised_id == supervised_id),
    ).get()
    if supervised is None:
        raise_errorcode(203)
    supervised.destroy()
