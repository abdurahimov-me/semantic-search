from fastapi import APIRouter
from fastapi_filter import FilterDepends

from resources.enums import LogModel, LogAction
from resources.filters import LogFilter
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
        service: services.LogService.annotated("db"),
        log_filter: LogFilter = FilterDepends(LogFilter)
):
    return await service.get_logs(log_filter)


@router.get(
    '/models/',
)
async def get_logs(
):
    return LogModel.as_dict_list()


@router.get(
    '/actions/',
)
async def get_logs(
):
    return LogAction.as_dict_list()


@router.get(
    '/users/',
    response_model=Page[schemas.LogSchema]
)
async def get_logs(
        service: services.LogService.annotated("db")
):
    return []
