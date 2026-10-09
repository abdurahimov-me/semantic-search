from fastapi import APIRouter

from .schemas import SearchRequest, SearchResponse
from .services import semantic_search

router = APIRouter(prefix='/search', tags=['Search'])


@router.post('', response_model=SearchResponse)
async def search(data: SearchRequest) -> SearchResponse:
    return await semantic_search(data)
