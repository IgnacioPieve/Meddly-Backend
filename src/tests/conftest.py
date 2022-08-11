import pytest
from fastapi import Depends, Header
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import app
from dependencies import auth, database
from models.user import User


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


app.dependency_overrides[auth.authenticate] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
