from fastapi import APIRouter

from utils.pagination import Page
from . import services, schemas

router = APIRouter(
    prefix='/log',
    tags=['log']
)


@router.get(
    '/',
    response_model=Page[schemas.LogSchema]
)
async def get_logs(
        service: services.LogService.annotated("db")
):
    return await service.get_logs()
