from typing import Optional
from models import Log
from fastapi_filter.contrib.sqlalchemy import Filter

from resources.enums import LogModel, LogAction



class LogFilter(Filter):
    model: Optional[LogModel] = None
    action: Optional[LogAction] = None
    executor_id: Optional[str] = None
    search: Optional[str] = None


    class Constants(Filter.Constants):
        model = Log
        search_model_fields = ("comment",)


