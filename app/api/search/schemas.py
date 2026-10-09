from typing import Annotated

from pydantic import BaseModel, Field, StringConstraints

from config import APP_SETTINGS


SearchText = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=APP_SETTINGS.MAX_TEXT_LENGTH),
]


class SearchRequest(BaseModel):
    text: SearchText
    limit: int = Field(default=APP_SETTINGS.DEFAULT_SEARCH_LIMIT, ge=1, le=50)
    score_threshold: float | None = Field(default=None, ge=-1, le=1)


class SearchResult(BaseModel):
    id: str
    text: str
    score: float
    score_percent: float


class SearchResponse(BaseModel):
    query: str
    total: int
    results: list[SearchResult]
