from typing import TypeVar

from fastapi import Query
from fastapi_pagination import Page as FastAPIPage, Params as FastAPIParams
from fastapi_pagination.customization import CustomizedPage, UseParams, UseFieldsAliases, UseExcludedFields

T = TypeVar("T")


class Params(FastAPIParams):
    size: int = Query(25, ge=1, le=500, alias="page_size")
    page: int = Query(1, ge=1)


Page = CustomizedPage[
    FastAPIPage[T],
    UseParams(Params),
    UseExcludedFields('size'),
    UseFieldsAliases(
        items="results",
        total="count",
        pages="total_pages",
    ),
]
