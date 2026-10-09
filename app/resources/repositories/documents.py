from __future__ import annotations

import typing as t
from qdrant_client import AsyncQdrantClient, models

from config import APP_SETTINGS
from config.qdrant import BaseRepository


class DocumentsRepository(BaseRepository):
    collection_name = APP_SETTINGS.DOCUMENTS_COLLECTION_NAME

    def __init__(self, qdrant_client: AsyncQdrantClient):
        super().__init__(qdrant_client)

    async def ensure_collection(self) -> bool:
        return await self.create_collection(
            models.VectorParams(
                size=APP_SETTINGS.EMBEDDING_SIZE,
                distance=models.Distance.COSINE,
            )
        )

    async def add_many(
            self,
            documents: t.Sequence[t.Tuple[str, t.List[float], t.Dict[str, t.Any]]],
    ) -> models.UpdateResult | None:
        points = [
            models.PointStruct(id=point_id, vector=vector, payload=payload)
            for point_id, vector, payload in documents
        ]
        return await self.upsert_many(points)

    async def list_all(self, *, page_size: int = 100) -> t.List[models.Record]:
        points: t.List[models.Record] = []
        offset = None
        while True:
            page, offset = await self.list(limit=page_size, offset=offset)
            points.extend(page)
            if offset is None:
                return points

    async def find_similar(
            self,
            vector: t.List[float],
            *,
            limit: int,
            score_threshold: float | None = None,
    ) -> t.List[models.ScoredPoint]:
        return await self.search(
            vector,
            limit=limit,
            score_threshold=score_threshold,
        )
