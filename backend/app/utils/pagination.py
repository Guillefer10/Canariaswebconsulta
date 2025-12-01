from typing import Any, List
from fastapi import Query


def pagination_params(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000)):
    return {"skip": skip, "limit": limit}


def paginate(queryset: List[Any], skip: int, limit: int):
    return queryset[skip : skip + limit]
