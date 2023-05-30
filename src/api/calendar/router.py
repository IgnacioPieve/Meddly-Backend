from datetime import datetime, timedelta

from fastapi import APIRouter, Depends

from api.auth.dependencies import authenticate_with_supervisor
from api.calendar.schemas import CalendarSchema
from api.calendar.service import get_calendar as get_calendar_service
from api.user.models import User

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get(
    "", response_model=CalendarSchema, status_code=200, summary="Get the calendar"
)
async def get_calendar(
    start: datetime = None,
    end: datetime = None,
    user: User = Depends(authenticate_with_supervisor),
):
    """
    Retrieves the calendar for a specific user within a date range.

    Args:
    - start (datetime, optional): The start date of the range. If not provided, it defaults to 15 days ago.
    - end (datetime, optional): The end date of the range. If not provided, it defaults to 15 days from now.
    - user (User, optional): The authenticated user. Defaults to Depends(authenticate_with_supervisor).

    Returns:
    - CalendarSchema: The calendar data.
    """

    if start is None:
        start = datetime.now() - timedelta(days=15)
    if end is None:
        end = datetime.now() + timedelta(days=15)
    calendar = await get_calendar_service(user, start, end)
    return calendar
