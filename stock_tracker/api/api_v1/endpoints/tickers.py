from typing import Any, List
from fastapi import APIRouter, HTTPException

from models import Ticker, Ticker_Pydantic, TickerIn_Pydantic


router = APIRouter()

@router.get("/", response_model=List[Ticker_Pydantic])
async def read_exchanges(skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieves a paginated list of stock tickers from database

    Args:
        skip (int, optional): Starting index for pagination. Defaults to 0.
        limit (int, optional): Number of records to retrieve. Defaults to 100.

    Returns:
        Any: List of Ticker objects
    """
    return await Ticker_Pydantic.from_queryset(Ticker.all().offset(skip).limit(limit))