from __future__ import annotations

import asyncio
import typing as t
from sentence_transformers import SentenceTransformer

from config import APP_SETTINGS


class EmbeddingEngine:
    def __init__(self) -> None:
        self._model: SentenceTransformer | None = None
        self._encode_lock = asyncio.Lock()

    @property
    def model(self) -> SentenceTransformer:
        if self._model is None:
            raise RuntimeError('Embedding model is not loaded')
        return self._model

    def load(self) -> None:
        if self._model is not None:
            return

        kwargs: t.Dict[str, t.Any] = {}
        if APP_SETTINGS.EMBEDDING_DEVICE:
            kwargs['device'] = APP_SETTINGS.EMBEDDING_DEVICE

        self._model = SentenceTransformer(
            APP_SETTINGS.EMBEDDING_MODEL_NAME,
            **kwargs,
        )

    async def encode_documents(self, texts: t.Sequence[str]) -> t.List[t.List[float]]:
        return await self._encode(texts)

    async def encode_query(self, text: str) -> t.List[float]:
        vectors = await self._encode([text], prompt_name='query')
        return vectors[0]

    async def _encode(
            self,
            texts: t.Sequence[str],
            *,
            prompt_name: str | None = None,
    ) -> t.List[t.List[float]]:
        async with self._encode_lock:
            vectors = await asyncio.to_thread(
                self.model.encode,
                list(texts),
                prompt_name=prompt_name,
                batch_size=APP_SETTINGS.EMBEDDING_BATCH_SIZE,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=False,
            )
        return vectors.tolist()


embedding_engine = EmbeddingEngine()
