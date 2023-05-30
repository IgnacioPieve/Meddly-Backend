from datetime import datetime

from api.appointment.service import get_appointments
from api.measurement.service import get_measurements
from api.medicine.service import get_consumptions
from api.user.models import User


async def get_calendar(user: User, start: datetime, end: datetime) -> dict:
    """
    Retrieves the calendar data for a specific user within a date range.

    Args:
        user (User): The user for whom to retrieve the calendar data.
        start (datetime): The start date of the range.
        end (datetime): The end date of the range.

    Returns:
        dict: The calendar data including consumptions, appointments, and measurements.
    """

    return {
        "consumptions": await get_consumptions(user, start, end),
        "appointments": await get_appointments(user, start, end),
        "measurements": await get_measurements(user, start, end),
    }
