import asyncio
from models import Exchange, Exchange_Pydantic, Ticker, Ticker_Pydantic, TickerIn_Pydantic
from scraping.scrape import get_all_tickers

async def save_ticker(ticker: dict, exchange: int) -> None:

    ticker["exchange_id"] = exchange
    ticker_in = await Ticker.get_or_create(**ticker)


async def load_tickers() -> None:
    print("in load tickers")
    exchanges = await Exchange_Pydantic.from_queryset(Exchange.all())

    for exchange in exchanges:
        code = exchange.code

        tickers = await get_all_tickers(exchange=code)

        print(len(tickers))

        for t in tickers:
            await save_ticker(t, exchange.id)

        