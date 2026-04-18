import logging

import grpc
from google.protobuf.json_format import MessageToDict
from google.protobuf.timestamp_pb2 import Timestamp

from config.db import db_helper
from models import Log
from ..stubs.log import log_pb2, log_pb2_grpc
from ..utils import dict_to_struct

logger = logging.getLogger(__name__)


class LogServicer(log_pb2_grpc.LogServiceServicer):

    async def CreateLog(self, request, context) -> log_pb2.LogResponse:
        try:
            async with db_helper.session() as session:
                log = Log(
                    instance_id=request.instance_id,
                    model=request.model,
                    executor_id=request.executor_id,
                    comment=request.comment,
                    action=request.action,
                    before=MessageToDict(request.before) if request.before else {},
                    after=MessageToDict(request.after) if request.after else {},
                    executor_data=MessageToDict(request.executor_data) if request.executor_data else {},
                )

                session.add(log)
                await session.commit()
                await session.refresh(log)

                # timestamp convert

                return log_pb2.LogResponse(
                    id=log.id,
                    model=log.model,
                    instance_id=log.instance_id,
                    executor_id=log.executor_id,
                    comment=log.comment or "",
                    action=log.action,
                    before=dict_to_struct(log.before),
                    after=dict_to_struct(log.after),
                    executor_data=dict_to_struct(log.executor_data),
                    created_at=str(log.created_at),
                )

        except Exception as e:
            logger.error(f'Error from CreateLog: {e}')
            return await context.abort(
                grpc.StatusCode.INTERNAL,
                str(e)
            )
