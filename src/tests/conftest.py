import pytest
from fastapi.testclient import TestClient

from api.auth.dependencies import authenticate
from api.user.service import assert_device, get_or_create_user
from app import app


async def override_auth():
    user = await get_or_create_user("test_user", "test_user@test.com")
    await assert_device(user, "test_device")
    return user


app.dependency_overrides[authenticate] = override_auth


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
