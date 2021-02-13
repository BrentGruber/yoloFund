import praw
import re
import requests_async as requests
from typing import List

from core.config import settings


async def get_all_tickers() -> List[str]:
    """
    Calls the Yahoo Finance API to retrieve a list of all stock tickers in
    the market
    """
    r = await requests.get(f'https://finnhub.io/api/v1/stock/symbol?exchange=US&token={settings.FINNHUB_API_KEY}', verify=False)
    return r.json()

async def get_ticker_mentions(subreddit: str, tickers: List[str]):
    """""
    Searches a subreddit to retrieve the top tickers mentioned

    Args:
        subreddit (str): subreddit to scrape
        tickers (List[str]): list of tickers to search for

    Returns:
        [type]: [description]
    """
    reddit = praw.Reddit(
        client_id=settings.REDDIT_CLIENT_ID,
        client_secret=settings.REDDIT_CLIENT_SECRET,
        user_agent="YoloFund",
    )
    weeklyTickers = {}

    for submission in reddit.subreddit("learnpython").hot(limit=10):
        print(submission.title)

    return True