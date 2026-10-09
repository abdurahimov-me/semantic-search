from fastapi import APIRouter, Response, status

from .schemas import DocumentsBatchCreate, DocumentsBatchResult, DocumentsList
from .services import add_documents, delete_document, list_documents

router = APIRouter(prefix='/documents', tags=['Documents'])


@router.get('', response_model=DocumentsList)
async def get_documents() -> DocumentsList:
    return await list_documents()


@router.post('/batch', response_model=DocumentsBatchResult, status_code=status.HTTP_201_CREATED)
async def create_documents(data: DocumentsBatchCreate) -> DocumentsBatchResult:
    return await add_documents(data)


@router.delete('/{document_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_document(document_id: str) -> Response:
    await delete_document(document_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
