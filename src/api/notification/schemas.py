from datetime import datetime
from typing import Literal

from pydantic import BaseModel


class NotificationSchema(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    type: Literal["supervisors", "appointment", "medicine"]
    is_read: bool

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Nuevo supervisado",
                "body": f"Has añadido a Ignacio como supervisado.",
                "created_at": datetime.now(),
                "type": "supervisors",
                "is_read": False,
            }
        }
