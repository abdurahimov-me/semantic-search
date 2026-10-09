from api.documents.router import router as documents_router
from api.search.router import router as search_router
from utils.routes import Routes

__routes__ = Routes(
    routers=(
        documents_router,
        search_router,
    )
)

__ws_routes__ = Routes(
    routers=(
    )
)
