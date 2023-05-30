import firebase_admin
from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

from api.auth.exceptions import ERROR203
from api.user.service import assert_device, get_or_create_user, get_user
from config import FIREBASE_JSON

firebase_cred = credentials.Certificate(FIREBASE_JSON)
firebase_admin.initialize_app(firebase_cred)


async def authenticate(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    device: str | None = Header(default=None),
):
    """
    Authenticate a user with a Bearer token.
    This does not support the supervisor role.
    """

    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
        )

    try:
        decoded_token = auth.verify_id_token(cred.credentials)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
        )

    user = await get_or_create_user(decoded_token["user_id"], decoded_token["email"])
    if device:
        await assert_device(user, device)
    return user


async def authenticate_with_supervisor(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    device: str | None = Header(default=None),
    supervised_id: str | None = Header(default=None),
):
    """
    Authenticate a user with a Bearer token.
    This supports the supervisor role.
    """
    user = await authenticate(cred, device=device)
    if supervised_id is not None:
        user = get_user(supervised_id)
        if not user:
            raise ERROR203
    return user
