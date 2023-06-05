import pytest
from fastapi.testclient import TestClient

from api.auth.dependencies import authenticate
from api.user.service import get_or_create_user
from app import app


async def override_auth(
    cred=None,
    device: str = None,
):
    user = await get_or_create_user("test_user", "test_user@test.com")
    if device:
        pass  # TODO
    return user


app.dependency_overrides[authenticate] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


print("AAAAAHI VA")
