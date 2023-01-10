import datetime

from pydantic import BaseModel, EmailStr


class UserUpdateSchema(BaseModel):
    first_name: str | None
    last_name: str | None
    height: float | None
    weight: float | None
    sex: bool | None
    birth: datetime.datetime | None
    phone: str | None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "first_name": "Ignacio",
                "last_name": "Pieve Roiger",
                "height": 170.0,
                "weight": 70.0,
                "sex": True,
                "birth": datetime.datetime(2000, 2, 10),
                "phone": "+5493512345678",
            }
        }


class UserSchema(UserUpdateSchema):
    id: str
    email: EmailStr
    invitation: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": "123456789",
                "email": "ignacio.pieve@gmail.com",
                "invitation": "AAA-B1B1-CCC",
                **UserUpdateSchema.Config.schema_extra["example"],
            }
        }
