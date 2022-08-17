from fastapi import APIRouter, Depends
from sqlalchemy import and_

from config import translations
from dependencies import auth
from models.user import Supervised
from schemas.user import UserSchema

router = APIRouter(prefix="/supervisors", tags=["Supervisors"])


@router.post(
    "/invitation",
    response_model=UserSchema,
    status_code=200,
    summary="Accept invitation",
)
def accept_invitation(code: str, authentication=Depends(auth.authenticate)):
    """
    Acepta un código de invitación
    """
    user, _ = authentication
    user.accept_invitation(code)
    return user


@router.delete(
    "/supervisor/{supervisor_id}",
    response_model=UserSchema,
    status_code=200,
    summary="Delete supervisor",
)
def delete_supervisor(supervisor_id: str, authentication=Depends(auth.authenticate)):
    """
    Elimina un supervisor
    """
    user, db = authentication
    supervisor = Supervised(
        db,
        and_(Supervised.supervisor_id == supervisor_id, Supervised.supervised == user),
    ).get()
    if supervisor is None:
        raise translations["errors"]["supervisors"]["supervisor_not_found"]
    supervisor.destroy()
    return user


@router.delete(
    "/supervised/{supervised_id}",
    response_model=UserSchema,
    status_code=200,
    summary="Delete supervised",
)
def delete_supervised(supervised_id: str, authentication=Depends(auth.authenticate)):
    """
    Elimina un supervisado
    """
    user, db = authentication
    supervised = Supervised(
        db,
        and_(Supervised.supervisor == user, Supervised.supervised_id == supervised_id),
    ).get()
    if supervised is None:
        raise translations["errors"]["supervisors"]["supervised_not_found"]
    supervised.destroy()
    return user
