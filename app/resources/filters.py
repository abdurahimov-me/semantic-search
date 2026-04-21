from typing import Optional
from models import Log
from fastapi_filter.contrib.sqlalchemy import Filter


class LogFilter(Filter):
    model: Optional[str] = None
    action: Optional[str] = None
    instance_id: Optional[str] = None


    class Constants(Filter.Constants):
        model = Log
        search_model_fields = ("comment",)


