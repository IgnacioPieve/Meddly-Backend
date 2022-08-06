from pydantic import BaseModel


class ResponseSchema(BaseModel):
    status_code: int
    message: str

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "message": 'Deletion successful'
            }
        }