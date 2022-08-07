from fastapi import FastAPI
import config
from routers import user, supervisors, test
from database import engine, Base

# ----- DATABASE -----
Base.metadata.create_all(bind=engine)

# ----- APP -----
app = FastAPI(**config.metadata)

# ----- ROUTERS -----
app.include_router(user.router)
app.include_router(supervisors.router)
app.include_router(test.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('app:app', host="0.0.0.0", port=8000, reload=True)
