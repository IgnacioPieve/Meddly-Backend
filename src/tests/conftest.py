import pytest
from fastapi.testclient import TestClient

from api.auth.dependencies import authenticate, authenticate_with_supervisor
from api.user.service import get_or_create_user
from app import app


class TestUser:
    def __init__(self, user_id="test"):
        self.user_id = user_id

    def get_header(self):
        return {"cred": self.user_id}


async def override_auth(
    cred=None,
    device: str = None,
):
    user = await get_or_create_user("test_user", "test_user@test.com")
    if device:
        pass  # TODO
    return user


app.dependency_overrides[authenticate] = override_auth
app.dependency_overrides[authenticate_with_supervisor] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


print("AAAAAHI VA")
