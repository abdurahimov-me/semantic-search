from utils.routes import Routes
from api.documents.router import router as documents_router
from api.search.router import router as search_router

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
