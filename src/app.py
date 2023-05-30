from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

import config
from api.appointment.router import router as appointment_router
from api.calendar.router import router as calendar_router
from api.dev_tools.router import router as dev_tools_router
from api.export.router import router as export_router
from api.image.router import router as image_router
from api.measurement.router import router as measurement_router
from api.medicine.router import router as medicine_router
from api.notification.router import router as notification_router
from api.prediction.router import router as prediction_router
from api.search.router import router as search_router
from api.supervisor.router import router as supervisor_router
from api.user.router import router as user_router
from database import Base, database, engine


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    await database.connect()
    yield
    # shutdown
    await database.disconnect()


# ----- DATABASE -----
Base.metadata.create_all(bind=engine)

# ----- APP -----
app = FastAPI(**config.metadata, lifespan=lifespan)

# ----- ROUTERS -----
routers = [
    dev_tools_router,
    user_router,
    supervisor_router,
    calendar_router,
    appointment_router,
    measurement_router,
    medicine_router,
    export_router,
    image_router,
    search_router,
    notification_router,
    prediction_router,
]

for router in routers:
    app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=11001, reload=True)
