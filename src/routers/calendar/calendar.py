import datetime

from fastapi import APIRouter, Depends

from dependencies import auth
from models.user import User
from schemas.calendar import CalendarSchema

router = APIRouter(prefix="/calendar")


@router.get("", response_model=CalendarSchema, status_code=200, include_in_schema=False)
@router.get(
    "/", response_model=CalendarSchema, status_code=200, summary="Get the calendar"
)
def get_calendar(
    start: datetime.date = None,
    end: datetime.date = None,
    authentication=Depends(auth.authenticate_with_supervisor),
):
    """
    Retorna todos los medicamentos del usuario logueado en un intervalo de tiempo.
    """
    user, _ = authentication
    user: User
    if start is None:
        start = datetime.datetime.now() - datetime.timedelta(days=15)
        end = datetime.datetime.now() + datetime.timedelta(days=15)
    return user.get_calendar(start, end)
