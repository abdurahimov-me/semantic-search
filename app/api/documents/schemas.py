from datetime import datetime
from pydantic import BaseModel, Field, StringConstraints, field_validator
from typing import Annotated

from config import APP_SETTINGS

TextValue = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=APP_SETTINGS.MAX_TEXT_LENGTH),
]


class TextCreate(BaseModel):
    text: TextValue


class DocumentsBatchCreate(BaseModel):
    items: list[TextCreate] = Field(
        min_length=1,
        max_length=APP_SETTINGS.MAX_BATCH_SIZE,
    )

    @field_validator('items')
    @classmethod
    def unique_texts(cls, items: list[TextCreate]) -> list[TextCreate]:
        seen: set[str] = set()
        for item in items:
            normalized = item.text.casefold()
            if normalized in seen:
                raise ValueError('Bir xil matnni bir batch ichida takrorlab bo‘lmaydi')
            seen.add(normalized)
        return items


class Document(BaseModel):
    id: str
    text: str
    created_at: datetime


class DocumentsBatchResult(BaseModel):
    added: int
    items: list[Document]


class DocumentsList(BaseModel):
    total: int
    items: list[Document]
