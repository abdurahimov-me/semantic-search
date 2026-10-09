from datetime import datetime, timezone
from fastapi import HTTPException, status
from uuid import uuid4

from config.qdrant import qdrant_db
from resources.embedding import embedding_engine
from resources.repositories import DocumentsRepository
from .schemas import Document, DocumentsBatchCreate, DocumentsBatchResult, DocumentsList


def get_repository() -> DocumentsRepository:
    return DocumentsRepository(qdrant_db.client)


def payload_to_document(point_id: str, payload: dict) -> Document:
    return Document(
        id=point_id,
        text=str(payload['text']),
        created_at=datetime.fromisoformat(str(payload['created_at'])),
    )


async def add_documents(data: DocumentsBatchCreate) -> DocumentsBatchResult:
    texts = [item.text for item in data.items]
    vectors = await embedding_engine.encode_documents(texts)
    created_at = datetime.now(timezone.utc)

    documents: list[Document] = []
    points = []
    for text, vector in zip(texts, vectors, strict=True):
        point_id = str(uuid4())
        payload = {'text': text, 'created_at': created_at.isoformat()}
        points.append((point_id, vector, payload))
        documents.append(payload_to_document(point_id, payload))

    await get_repository().add_many(points)
    return DocumentsBatchResult(added=len(documents), items=documents)


async def list_documents() -> DocumentsList:
    records = await get_repository().list_all()
    documents = [
        payload_to_document(str(record.id), record.payload or {})
        for record in records
        if record.payload and record.payload.get('text') and record.payload.get('created_at')
    ]
    documents.sort(key=lambda item: item.created_at, reverse=True)
    return DocumentsList(total=len(documents), items=documents)


async def delete_document(document_id: str) -> None:
    deleted = await get_repository().delete(document_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Matn topilmadi',
        )
