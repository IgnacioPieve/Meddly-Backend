from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from dependencies import auth, database
from schemas.user import UserSchema, UserUpdateSchema
from schemas.utils import GenericResponseSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=UserSchema, status_code=200, summary="Get user data")
async def get_user(authentication=Depends(auth.authenticate)):
    """
    Obtener la información de un usuario
    """
    user, _ = authentication
    return user


@router.post("/", response_model=UserSchema, status_code=200, summary="Update user data")
async def update_user(
        update_data: UserUpdateSchema,
        authentication=Depends(auth.authenticate)
):
    """
    Actualiza los datos de un usuario (sobreecribiendo el objeto completo).
    """
    user, _ = authentication
    for key, value in update_data:
        setattr(user, key, value)
    user.save()
    return user


@router.delete("/", response_model=GenericResponseSchema, status_code=200, summary="Delete user")
async def delete_user(
        authentication=Depends(auth.authenticate)
):
    """
    Elimina completamente a un usuario
    """
    user, _ = authentication
    user.destroy()
    return {
        "status_code": 200,
        "message": 'Success'
    }
