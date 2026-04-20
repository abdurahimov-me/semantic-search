import typing as t

from pydantic import BaseModel


class LogSchema(BaseModel):
    id: int
    model: int
    action: int
    instance_id: str
    executor_id: str
    before: t.Optional[dict]
    after: t.Optional[dict]
    executor_data: t.Optional[dict]
    comment: t.Optional[str]

    class Config:
        from_attributes = True
