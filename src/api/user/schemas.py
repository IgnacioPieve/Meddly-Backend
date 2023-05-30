# TODO: Refactored: True

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


class UserSchema(UserUpdateSchema):
    id: str
    email: EmailStr
    invitation: str

    class Config:
        orm_mode = True
