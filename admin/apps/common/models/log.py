__all__ = (
    "Log",
)
from django.db import models

from .base import BaseModel


class Log(BaseModel):
    updated_at = None

    model = models.SmallAutoField()
    action = models.SmallAutoField()
    instance_id = models.CharField(max_length=255)
    executor_id = models.CharField(max_length=255)
    before = models.JSONField(default=dict, null=True, blank=True)
    after = models.JSONField(default=dict, null=True, blank=True)
    executor_data = models.JSONField(default=dict, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'logs'
