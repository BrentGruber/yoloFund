from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI
from tortoise import Tortoise
import ssl
import uvicorn

from api.api_v1.api import api_router
from core.config import settings
from scraping.finnhub import get_all_tickers
from scheduled.tickers import load_tickers

app = FastAPI()


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