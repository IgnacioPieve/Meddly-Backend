import traceback

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

import config
from database import Base, engine
from routers import notification, supervisor, test, treatment, user

# ----- DATABASE -----
Base.metadata.create_all(bind=engine)

# ----- APP -----
app = FastAPI(**config.metadata)

# ----- ROUTERS -----
app.include_router(user.router)
app.include_router(supervisor.router)
app.include_router(treatment.router)
app.include_router(notification.router)
app.include_router(test.router)


# ----- EXCEPTIONS MIDDLEWARE -----
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        body = {
            'message': 'Internal server error',
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        return Response(body, status_code=500)


app.middleware('http')(catch_exceptions_middleware)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
