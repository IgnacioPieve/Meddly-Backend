from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from api.auth.dependencies import authenticate
from api.calendar.schemas import CalendarSchema
from api.calendar.service import get_calendar as get_calendar_service
from api.supervisor.exceptions import ERROR205
from api.supervisor.service import get_supervised
from api.user.models import User
from api.user.service import get_user

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get(
    "", response_model=CalendarSchema, status_code=200, summary="Get the calendar"
)
async def get_calendar(
    users: Annotated[list[str] | None, Query()] = None,
    start: datetime = None,
    end: datetime = None,
    user: User = Depends(authenticate),
):
    """
    Retrieves the calendar for a specific user within a date range.

    Args:
    - start (datetime, optional): The start date of the range. If not provided, it defaults to 15 days ago.
    - end (datetime, optional): The end date of the range. If not provided, it defaults to 15 days from now.
    - user (User, optional): The authenticated user. Defaults to Depends(authenticate_with_supervisor).

    Returns:
    - CalendarSchema: The calendar data.

    TODO: Update this docstring
    """

    if start is None:
        start = datetime.now() - timedelta(days=15)
    if end is None:
        end = datetime.now() + timedelta(days=15)

    user_id = user.id
    supervised_users_ids = [supervised.id for supervised in await get_supervised(user)]
    user_objects = []

    if not users:
        users = supervised_users_ids + [user_id]
    else:
        users = set(users)

    for user in users:
        if user not in supervised_users_ids and user != user_id:
            raise ERROR205
        user_objects.append(await get_user(user))

    calendar = {}
    for user in user_objects:
        calendar[user.id] = await get_calendar_service(user, start, end)

    return calendar
