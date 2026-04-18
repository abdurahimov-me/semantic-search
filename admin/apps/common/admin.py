from django.contrib import admin

from . import models


@admin.register(models.Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("id", "action", "model", "instance_id", "comment", "executor_id", "executor", "created_at")
    search_fields = ("comment",)
    list_filter = ("action", "model", "executor_id", "instance_id")
