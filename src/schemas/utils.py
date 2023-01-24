from pydantic import BaseModel


class SearchResultSchema(BaseModel):
    results: list[str]


class ProbabilitySchema(BaseModel):
    disease: str
    probability: float

