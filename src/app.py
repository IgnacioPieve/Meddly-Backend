import json
import time
import traceback
from typing import Callable

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response

import config
from database import Base, engine
from routers import calendar, notification, supervisor, test, user

# ----- DATABASE -----
Base.metadata.create_all(bind=engine)

# ----- APP -----
app = FastAPI(**config.metadata)

# ----- ROUTERS -----
app.include_router(user.router)
app.include_router(supervisor.router)
app.include_router(calendar.router)
app.include_router(notification.router)
app.include_router(test.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
