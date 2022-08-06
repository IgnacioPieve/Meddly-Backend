from fastapi import FastAPI
import config
from routers import test

app = FastAPI(**config.metadata)

# ----- ROUTERS -----
app.include_router(test.router)

