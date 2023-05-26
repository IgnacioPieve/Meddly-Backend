from user_calendar import router as calendar_router

from fastapi import FastAPI

import config
from database import Base, engine
from dev_tools import router as dev_tools_router
from export import router as export_router
from image import router as image_router
from notification import router as notification_router
from prediction import router as prediction_router
from search import router as search_router
from supervisor import router as supervisor_router
from user import router as user_router

# ----- DATABASE -----
Base.metadata.create_all(bind=engine)

# ----- APP -----
app = FastAPI(**config.metadata)

# ----- ROUTERS -----
app.include_router(dev_tools_router.router)

app.include_router(calendar_router.router)
app.include_router(export_router.router)
app.include_router(image_router.router)
app.include_router(notification_router.router)
app.include_router(prediction_router.router)
app.include_router(search_router.router)
app.include_router(supervisor_router.router)
app.include_router(user_router.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=11001, reload=True)
