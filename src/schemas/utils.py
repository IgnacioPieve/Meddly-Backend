from pydantic import BaseModel


class SearchResultSchema(BaseModel):
    results: list[str]


