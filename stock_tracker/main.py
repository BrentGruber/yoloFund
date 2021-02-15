from apscheduler.schedulers.asyncio import AsyncIOScheduler

from fastapi import FastAPI, Request
from tortoise import Tortoise
import ssl
import uvicorn
import time

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

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """
    Adds an X-Process-Time header to response with how long the call took to execute
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

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