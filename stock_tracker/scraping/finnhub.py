import re
import requests_async as requests
from typing import List

from core.config import settings


async def get_all_tickers(exchange: str) -> List[dict]:
    """
    Calls the Yahoo Finance API to retrieve a list of all stock tickers in
    the market

    Args:
        exchange (str): exchange for which to retrieve all tickers from

    Returns:
        List[dict]: A list of all ticker information for the exchange
    """
    r = await requests.get(f'https://finnhub.io/api/v1/stock/symbol?exchange={exchange}&token={settings.FINNHUB_API_KEY}', verify=False)
    return r.json()