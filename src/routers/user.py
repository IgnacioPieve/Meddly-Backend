from fastapi import APIRouter, Depends
from requests import Session

from dependencies import auth, database
from schemas.user import UserSchema, UserUpdateSchema
from schemas.utils import ResponseSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", response_model=UserSchema, status_code=200, summary="Get user data")
async def get_user(user=Depends(auth.authenticate)):
    """
    Obtener la información de un usuario
    """
    return user


@router.post("/", response_model=UserSchema, status_code=200, summary="Update user data")
async def update_user(
        update_data: UserUpdateSchema,
        user=Depends(auth.authenticate),
        db: Session = Depends(database.get_db),
):
    """
    Actualiza los datos de un usuario (sobreecribiendo el objeto completo).
    """
    for key, value in update_data:
        setattr(user, key, value)
    user.save(db)
    return user


@router.delete("/", response_model=ResponseSchema, status_code=200, summary="Delete user")
async def delete_user(
        user=Depends(auth.authenticate),
        db: Session = Depends(database.get_db),
):
    """
    Elimina completamente a un usuario
    """
    user.destroy(db)
    return {
        "status_code": 200,
        "message": 'Deletion successful'
    }
