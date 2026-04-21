import typing as t

from pydantic import BaseModel

from utils.customs import DateTime


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
    created_at: DateTime

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: str
    executor_data: t.Optional[dict]

    class Config:
        from_attributes = True
