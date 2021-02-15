from typing import Any, List
from fastapi import APIRouter, HTTPException

from models import Exchange, Exchange_Pydantic, ExchangeIn_Pydantic


router = APIRouter()

@router.get("/", response_model=List[Exchange_Pydantic])
async def read_exchanges(skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieves a paginated list of stock exchanges from database

    Args:
        skip (int, optional): Starting index for pagination. Defaults to 0.
        limit (int, optional): Number of records to retrieve. Defaults to 100.

    Returns:
        Any: List of Exchange objects
    """
    return await Exchange_Pydantic.from_queryset(Exchange.all().offset(skip).limit(limit))

@router.post("/", response_model=Exchange_Pydantic)
async def create_exchange(body: ExchangeIn_Pydantic) -> Any:
    """
    Create an exchange to retrieve stock tickers from

    Args:
        body (ExchangeIn_Pydantic): Information about stock exchange to add

    Returns:
        [type]: Exchange object which was added to db
    """
    exchg = await Exchange.create(**body.dict(exclude_unset=True))
    return await Exchange_Pydantic.from_tortoise_orm(exchg)