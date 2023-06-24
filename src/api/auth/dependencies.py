from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth

from api.user.models import User
from api.user.service import assert_device, get_or_create_user


async def authenticate(
    cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
    device: str | None = Header(default=None),
) -> User:  # pragma: no cover
    """
    Authenticate a user with a Bearer token.

    Args:
        cred (HTTPAuthorizationCredentials): The HTTP authorization credentials.
        device (str | None): The device header. Defaults to None and represents the device_id used to authenticate.
                            It is used to send push notifications to the device.

    Raises:
        HTTPException: If bearer authentication is required or if the authentication credentials are invalid.

    Returns:
        User: The authenticated user.
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

    user: User = await get_or_create_user(
        decoded_token["user_id"], decoded_token["email"]
    )
    if device:
        await assert_device(user, device)
    return user
