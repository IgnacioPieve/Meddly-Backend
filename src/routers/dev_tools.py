import requests
from fastapi import APIRouter

from config import FIREBASE_JSON
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/dev", tags=["Developer_Tools"])


class UserRequestModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        schema_extra = {"example": {"email": "test@test.com", "password": "password"}}


@router.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@router.post("/login")
def login(user: UserRequestModel):
    user = {**user.dict(), "returnSecureToken": True}
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_JSON['key']}"
    response = requests.post(url, json=user)
    try:
        return {"status": "ok", "token": response.json()["idToken"]}
    except KeyError:
        print(response.json())


# Endpoint to register user
@router.post("/register")
def register(user: UserRequestModel):
    user = {**user.dict(), "returnSecureToken": True}
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={FIREBASE_JSON['key']}"
    response = requests.post(url, json=user)
    try:
        return {"status": "ok", "token": response.json()["idToken"]}
    except KeyError:
        print(response.json())


@router.post("/reset-database")
def reset_database():
    from database import Base, engine

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    return {"status": "ok"}
