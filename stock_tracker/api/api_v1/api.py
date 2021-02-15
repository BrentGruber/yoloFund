
from fastapi import APIRouter

from api.api_v1.endpoints import exchanges, tickers

api_router = APIRouter()

api_router.include_router(exchanges.router, prefix="/exchanges", tags=["Exchanges"])
api_router.include_router(tickers.router, prefix="/tickers", tags=["Tickers"])