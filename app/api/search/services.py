from config.qdrant import qdrant_db
from resources.embedding import embedding_engine
from resources.repositories import DocumentsRepository
from .schemas import SearchRequest, SearchResponse, SearchResult


async def semantic_search(data: SearchRequest) -> SearchResponse:
    vector = await embedding_engine.encode_query(data.text)
    matches = await DocumentsRepository(qdrant_db.client).find_similar(
        vector,
        limit=data.limit,
        score_threshold=data.score_threshold,
    )

    results = []
    for match in matches:
        payload = match.payload or {}
        if not payload.get('text'):
            continue
        score = float(match.score)
        results.append(
            SearchResult(
                id=str(match.id),
                text=str(payload['text']),
                score=score,
                score_percent=round(max(0.0, min(1.0, score)) * 100, 2),
            )
        )

    return SearchResponse(query=data.text, total=len(results), results=results)
