__all__ = (
    "Log",
)
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from utils.customs.fields import IntEnumField
from .base import BaseModel
from resources.enums import LogAction, LogModel

class Log(BaseModel):
    __tablename__ = 'logs'
    updated_at = None
    model: Mapped[int] = mapped_column(
        IntEnumField(LogModel),
        index=True,
    )
    action: Mapped[int] = mapped_column(
        IntEnumField(LogAction),
        index=True,
    )
    instance_id: Mapped[str] = mapped_column(
        sa.String(255),
        index=True,
    )
    executor_id: Mapped[str] = mapped_column(
        sa.String(255),
        index=True,
    )
    before: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
        default=dict(),
    )
    after: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
        default=dict(),
    )
    executor_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True,
    )
    comment: Mapped[str] = mapped_column(
        sa.Text(),
        nullable=True,
    )
