from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI
from tortoise import Tortoise
import uvicorn

from api.api_v1.api import api_router
from core.config import settings
from scraping.scrape import get_all_tickers, get_ticker_mentions
from scheduled.tickers import load_tickers

app = FastAPI()


from models import Ticker, TickerIn_Pydantic, Ticker_Pydantic


@app.get("/ticker-mentions")
async def check_tickers():
    tickers = await Ticker_Pydantic.from_queryset(Ticker.all())

    ticker_list = [t.symbol for t in tickers]

    mentions = await get_ticker_mentions("RobinhoodPennyStocks", ticker_list)
    return zip(*sorted(mentions.items()))

app.include_router(api_router, prefix=settings.API_V1_STR)

TORTOISE_CONFIG = {
    "connections": {"default": f"{settings.DATABASE_URI}"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default"
        }
    },
    "use_tz": False,
    "timezone": "UTC"
}

@app.on_event("startup")
async def startup_event():
    """
    Startup event
    """
    await Tortoise.init(
        config=TORTOISE_CONFIG
    )

    scheduler = AsyncIOScheduler()
    print("ADDING JOB TO SCHEDULER")
    scheduler.add_job(load_tickers, 'interval', minutes=10)
    scheduler.start()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)