from fastapi import FastAPI, APIRouter

import config
from database import Base, engine
from routers import calendar, notification, supervisor, dev_tools, user

# ----- DATABASE -----
Base.metadata.create_all(bind=engine)

# ----- APP -----
app = FastAPI(**config.metadata)

# ----- ROUTERS -----
app.include_router(user.router)
app.include_router(supervisor.router)
app.include_router(calendar.router)
app.include_router(notification.router)
app.include_router(dev_tools.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
