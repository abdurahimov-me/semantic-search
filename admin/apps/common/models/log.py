__all__ = (
    "Log",
)

from django.db import models

from .base import BaseModel


class ModelChoices(models.IntegerChoices):
    ORDER = 1, "Order"
    USER = 2, "User"
    CLIENT = 3, "Client"
    OFFER = 5, "Offer"


class ActionChoices(models.IntegerChoices):
    CREATE = 1, "Create"
    UPDATE = 2, "Update"
    DELETE = 3, "Delete"
    LOGIN = 4, "Login"
    LOGOUT = 5, "Logout"


class Log(BaseModel):
    updated_at = None

    model = models.SmallIntegerField(choices=ModelChoices.choices)
    action = models.SmallIntegerField(choices=ActionChoices.choices)
    instance_id = models.CharField(max_length=255)
    executor_id = models.CharField(max_length=255)
    before = models.JSONField(default=dict, null=True, blank=True)
    after = models.JSONField(default=dict, null=True, blank=True)
    executor_data = models.JSONField(default=dict, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'logs'
