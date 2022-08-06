import requests
from fastapi import APIRouter, Depends
from schemas.test import UserRequestModel
from config import FIREBASE_JSON

router = APIRouter(prefix="/test", tags=["Test"])


@router.get("/status")
def get_status():
    """Get status of messaging server."""
    return {"status": "running"}


@router.post("/login")
def login(user: UserRequestModel):
    user = {**user.dict(), "returnSecureToken": True}
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={FIREBASE_JSON['key']}"
    response = requests.post(url, json=user)
    return {"status": "ok", "token": response.json()["idToken"]}


# Endpoint to register user
@router.post("/register")
def register(user: UserRequestModel):
    user = {**user.dict(), "returnSecureToken": True}
    url = f"https://www.googleapis.com/identitytoolkit/v3/relyingparty/signupNewUser?key={FIREBASE_JSON['key']}"
    response = requests.post(url, json=user)
    return {"status": "ok", "token": response.json()["idToken"]}
