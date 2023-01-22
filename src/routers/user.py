from fastapi import APIRouter, Depends

from dependencies import auth
from schemas.user import UserSchema, UserUpdateSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.get("", response_model=UserSchema, status_code=200, include_in_schema=False)
@router.get("/", response_model=UserSchema, status_code=200, summary="Get user data")
async def get_user(authentication=Depends(auth.authenticate)):
    """
    Obtener la información de un usuario
    """
    user, _ = authentication
    return user


@router.post("", status_code=200, include_in_schema=False)
@router.post("/", status_code=200, summary="Update user data")
async def update_user(update_data: UserUpdateSchema, authentication=Depends(auth.authenticate)):
    """
    Actualiza los datos de un usuario (sobreecribiendo el objeto completo).
    """
    user, _ = authentication
    for key, value in update_data:
        setattr(user, key, value)
    user.save()


@router.delete("", status_code=200, include_in_schema=False)
@router.delete("/", status_code=200, summary="Delete user")
async def delete_user(authentication=Depends(auth.authenticate)):
    """
    Elimina completamente a un usuario
    """
    user, _ = authentication
    user.destroy()
