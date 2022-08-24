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
from routers import notification, supervisor, test, treatment, user

# ----- DATABASE -----
Base.metadata.create_all(bind=engine)

# ----- APP -----
app = FastAPI(**config.metadata)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        body = {
            "message": "An error occurred while handling the request",
            "error": str(e),
            "traceback": traceback.format_exc(),
        }
        return Response(
            status_code=500, content=json.dumps(body), media_type="application/json"
        )


# ----- ROUTERS -----
app.include_router(user.router)
app.include_router(supervisor.router)
app.include_router(treatment.router)
app.include_router(notification.router)
app.include_router(test.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
