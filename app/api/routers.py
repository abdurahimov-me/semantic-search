from utils.routes import Routes
from .log.router import router

__routes__ = Routes(
    routers=(
        router,
    )
)

__ws_routes__ = Routes(
    routers=(
    )
)
