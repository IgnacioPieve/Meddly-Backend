import datetime

from pydantic import BaseModel, EmailStr

from schemas.example_data import example_profile


class SupervisorSchema(BaseModel):
    # This is a Response Schema.
    id: str
    email: EmailStr
    name: str | None
    avatar: str | None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": example_profile.id(),
                "email": example_profile.email(),
                "name": f"{example_profile.first_name()} {example_profile.last_name()}",
                "avatar": example_profile.avatar(),
            }
        }


class UserUpdateSchema(BaseModel):
    # This an Input Schema.
    name: str | None
    height: float | None
    weight: float | None
    sex: str | None
    birth: datetime.datetime | None
    avatar: str | None
    phone: int | None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": f"{example_profile.first_name()} {example_profile.last_name()}",
                "height": example_profile.height(),
                "weight": example_profile.weight(),
                "sex": example_profile.sex(),
                "avatar": example_profile.avatar(),
                "phone": example_profile.phone(),
            }
        }


class UserSchema(UserUpdateSchema):
    # This is a Response Schema.
    id: str
    email: EmailStr
    created_at: datetime.datetime
    updated_at: datetime.datetime
    # diseases: list[str]
    supervisors: list[SupervisorSchema]
    supervised: list[SupervisorSchema]
    notification_preferences: list[str]
    invitation: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": example_profile.id(),
                "email": example_profile.email(),
                "created_at": example_profile.created_at(),
                "updated_at": example_profile.updated_at(),
                "invitation": example_profile.invitation(),
                "notification_preferences": example_profile.notification_preferences(),
                **UserUpdateSchema.Config.schema_extra["example"],
                "supervisors": [
                    {
                        **SupervisorSchema.Config.schema_extra["example"],
                    },
                ],
                "supervised": [
                    {
                        **SupervisorSchema.Config.schema_extra["example"],
                    },
                ],
                # "diseases": ["diabetes", "hipertension"],
            }
        }
