import asyncio

import grpc

from config.settings import APP_SETTINGS
from resources.integrations.grpc.servicers import (
    LogServicer,
)
from resources.integrations.grpc.stubs.log import log_pb2_grpc


async def serve():
    server = grpc.aio.server(
        options=[
            ('grpc.keepalive_time_ms', 10000),
            ('grpc.keepalive_timeout_ms', 5000),
            ('grpc.keepalive_permit_without_calls', 1),
            ('grpc.http2.max_pings_without_data', 0),
            ('grpc.http2.min_ping_interval_without_data_ms', 5000),
            ('grpc.max_connection_idle_ms', 600000),
            ('grpc.max_connection_age_ms', 900000),
            ('grpc.max_connection_age_grace_ms', 10000),
        ]
    )

    log_pb2_grpc.add_LogServiceServicer_to_server(
        LogServicer(), server
    )

    server.add_insecure_port(f"[::]:{APP_SETTINGS.GRPC_PORT}")

    await server.start()
    print(f"✅ Async gRPC server started on port {APP_SETTINGS.GRPC_PORT}")

    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
