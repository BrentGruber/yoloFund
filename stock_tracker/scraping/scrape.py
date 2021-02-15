import praw
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
    dailyTickers = {}

    regexPattern = r'\b([A-Z]+)\b'
    blacklist = ["A", "I", "DD", "WSB", "YOLO", "RH", "EV", "PE", "ETH", "BTC", "E"]
    for submission in reddit.subreddit(subreddit).top("day"):
        strings = [submission.title]
        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            strings.append(comment.body)
        for s in strings:
            for phrase in re.findall(regexPattern, s):
                if phrase not in blacklist:
                    if phrase in tickers:
                        dailyTickers[phrase] = dailyTickers.get(phrase, 0) + 1

    return dailyTickers


    return True