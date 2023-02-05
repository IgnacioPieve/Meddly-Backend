import firebase_admin
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials
from sqlalchemy.orm import Session

from config import FIREBASE_JSON
from dependencies import database
from models.user import User, Supervised
from models.utils import raise_errorcode

cred = credentials.Certificate(FIREBASE_JSON)
firebase_admin.initialize_app(cred)


async def authenticate(
        cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        db: Session = Depends(database.get_db),
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
    user: User = User(db, User.id == decoded_token["user_id"]).get()
    if not user:
        user = User(
            db, id=decoded_token["user_id"], email=decoded_token["email"]
        ).create()
    return user, db


async def authenticate_with_supervisor(
        cred: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        db=Depends(database.get_db),
        supervised_id: str | None = Header(default=None),
):
    """
    Authenticate a user with a Bearer token.
    This supports the supervisor role.
    """
    user, db = await authenticate(cred, db)
    if supervised_id is not None:
        supervised = Supervised(db,
                                Supervised.supervisor == user,
                                Supervised.supervised_id == supervised_id).get()
        if supervised is None:
            raise_errorcode(203)
        user = supervised.supervised
    return user, db
