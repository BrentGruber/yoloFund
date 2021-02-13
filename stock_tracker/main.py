from fastapi import FastAPI
from tortoise import Tortoise
import uvicorn

from core.config import settings
from reddit.scrape import get_all_tickers, get_ticker_mentions

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/tickers")
async def tickers():
    return await get_all_tickers()

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
    print(settings.DATABASE_URI)
    await Tortoise.init(
        config=TORTOISE_CONFIG
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)