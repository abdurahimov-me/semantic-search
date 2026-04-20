from resources.services.http import BaseHTTPService
from models import Log
import sqlalchemy as sa
from fastapi_pagination.ext.sqlalchemy import apaginate

class LogService(BaseHTTPService):

    async def get_logs(self):
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
        data = await apaginate(self.db, stmt)
        return data



