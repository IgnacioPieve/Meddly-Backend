from user_calendar.router.appointment import router as appointment_router

from fastapi import APIRouter
from user_calendar.router.calendar import router as calendar_router
from user_calendar.router.measurement import router as measurement_router
from user_calendar.router.medicine import router as medicine_router

router = APIRouter(prefix="/calendar", tags=["Calendar"])
router.include_router(calendar_router)
router.include_router(appointment_router)
router.include_router(medicine_router)
router.include_router(measurement_router)
