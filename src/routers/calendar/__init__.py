from fastapi import APIRouter

from routers.calendar.appointment import router as appointment_router
from routers.calendar.calendar import router as calendar_router
from routers.calendar.medicine import router as medicine_router

router = APIRouter(tags=["Calendar"])
router.include_router(calendar_router)
router.include_router(appointment_router)
router.include_router(medicine_router)
