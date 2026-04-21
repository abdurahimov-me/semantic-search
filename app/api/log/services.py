import sqlalchemy as sa
from fastapi_pagination.ext.sqlalchemy import apaginate

from models import Log
from resources.filters import LogFilter
from resources.services.http import BaseHTTPService


class LogService(BaseHTTPService):

    async def get_logs(self, log_filter: LogFilter):
        stmt = sa.select(
            Log.id,
            Log.created_at,
            Log.model,
            Log.action,
            Log.instance_id,
            Log.executor_id,
            Log.before,
            Log.after,
            Log.executor_data,
            Log.comment,
        )

        stmt = log_filter.filter(stmt).order_by(Log.id.desc())

        data = await apaginate(self.db, stmt, unique=False)
        return data
