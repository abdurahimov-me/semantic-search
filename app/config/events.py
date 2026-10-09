import asyncio

from fastapi import FastAPI

from config.qdrant import qdrant_db
from resources.embedding import embedding_engine
from resources.repositories import DocumentsRepository


async def on_startup(app: FastAPI) -> None:
    await qdrant_db.connect()
    app.state.qdrant = qdrant_db.client
    await DocumentsRepository(qdrant_db.client).ensure_collection()
    await asyncio.to_thread(embedding_engine.load)


async def on_shutdown(app: FastAPI) -> None:
    await qdrant_db.close()
