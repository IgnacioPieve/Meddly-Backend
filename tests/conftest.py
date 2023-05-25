import pytest
from dependencies import database
from fastapi import Depends, Header
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import app
from auth.dependencies import authenticate
from user.models import User


class TestUser:
    def __init__(self, user_id="test"):
        self.user_id = user_id

    def get_header(self):
        return {"cred": self.user_id}


async def override_auth(
    cred: str = Header(default=None), db: Session = Depends(database.get_db)
):
    decoded_token = {"user_id": cred, "email": f"{cred}@test.com"}
    user: User = User(db, User.id == decoded_token["user_id"]).get()
    if not user:
        user = User(
            db, id=decoded_token["user_id"], email=decoded_token["email"]
        ).create()
    return user, db


app.dependency_overrides[authenticate] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
