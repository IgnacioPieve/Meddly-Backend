import asyncio
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
    "", response_model=CalendarSchema, status_code=200, summary="Get users calendar"
)
async def get_calendar(
    users: Annotated[list[str] | None, Query()] = None,
    start: datetime = None,
    end: datetime = None,
    user: User = Depends(authenticate),
):
    """
    # Get users calendar

    Retrieve the calendar for the specified users within the given time frame.

    Args:
    - **users** (optional): A list of user IDs to retrieve the calendar for.
                            This parameter is only available to supervised users and the authenticated user.
                            If not provided, the calendar will be retrieved for
                            the authenticated user and their supervised users.
    - **start** (optional): The start date and time of the calendar range. Defaults to 15 days ago if not provided.
    - **end** (optional): The end date and time of the calendar range. Defaults to 15 days from now if not provided.
    - **user** (User): The authenticated user. This parameter is automatically obtained from the request.

    Returns:
    - **CalendarSchema**: A dictionary containing the calendar data for each user, keyed by their user ID.
    """

    start = start or datetime.now() - timedelta(days=15)
    end = end or datetime.now() + timedelta(days=15)

    supervised_users_ids = list(
        {supervised.id for supervised in await get_supervised(user)}
    )
    users_to_get_calendar = users or (supervised_users_ids + [user.id])

    if any(
        user_to_get_calendar not in supervised_users_ids
        and user_to_get_calendar != user.id
        for user_to_get_calendar in users_to_get_calendar
    ):
        raise ERROR205

    user_objects = await asyncio.gather(
        *[
            get_user(user_to_get_calendar)
            for user_to_get_calendar in users_to_get_calendar
        ]
    )
    calendar = {
        user.id: await get_calendar_service(user, start, end) for user in user_objects
    }

    return calendar
