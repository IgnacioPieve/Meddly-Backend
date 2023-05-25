from pydantic import BaseModel


class SearchResultSchema(BaseModel):
    code: str
    description: str
