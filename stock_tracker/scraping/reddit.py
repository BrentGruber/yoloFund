import asyncio
import aiohttp
import asyncpraw
import re
import ssl
from typing import Dict, List

from core.config import settings


class Reddit():

    @classmethod
    async def create(cls):
        """
        Initialize the class with an asyncpraw connection

        Args:
            settings ([type]): [description]
        """
        self = Reddit()

        ssl_ctx = ssl._create_unverified_context()

        conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
        session = aiohttp.ClientSession(connector=conn)
        self.reddit = asyncpraw.Reddit(
            client_id=settings.REDDIT_CLIENT_ID,
            client_secret=settings.REDDIT_CLIENT_SECRET,
            user_agent="YoloFund",
            requestor_kwargs={"session": session},
        )

        self.ticker_re = r'\b([A-Z]+)\b'
        self.blacklist = ["A", "I", "DD", "WSB", "YOLO", "RH", "EV", "PE", "ETH", "BTC", "E", "HOLD", "CEO"]
        return self

    def _get_matches(self, s: str, tickers: List[str]) -> Dict[str, int]:
        """
        Check a single string for regular expression matches

        Args:
            s (str): string to check for re matches
            tickers (List[str]): list of tickers to check against

        Returns:
            Dict[str, int]: Dictionary contianing re matches and their counts
        """
        retval = {}

        for phrase in re.findall(self.ticker_re, s):
            if phrase not in self.blacklist and phrase in tickers:
                retval[phrase] = retval.get(phrase, 0) + 1
        
        return retval

    async def _get_comment_tickers(self, comment: asyncpraw.models.Comment, tickers: List[str]):
        """
        Parses a single comment in a reddit post and counts the number of times a regular expression occurs

        Args:
            comment (asyncpraw.Comment): The reddit comment to parse
            tickers (List[str]): The list of stock tickers to check against

        Returns:
            Dict[str, int]: A dictionary which maps the stock ticker to the count of times it occurs
        """
        retval = {}

        for phrase in re.findall(self.ticker_re, comment.body):
            if phrase not in self.blacklist and phrase in tickers:
                if retval.get(phrase):
                    retval[phrase]["mentions"] = retval.get('mentions',[]).append({"location": "comment", "id": comment.id})
                    retval[phrase]["count"] = retval.get(phrase).get("count", 0) + 1
                else:
                    retval[phrase] = {
                        "mentions": [{"location": "comment", "id": comment.id}],
                        "count": 1
                    }
        
        return retval

    async def _get_submission_tickers(self, submission: asyncpraw.models.Submission, tickers: List[str]):
        """
        Parses a submission in reddit and counts the number of times a regular expression occurs

        Args:
            submission (asyncpraw.Submission): reddit submission to parse
            tickers (List[str]): list of stock tickers to check against

        Returns:
            Dict[str, int]: Dictionary with count of occurrences for each ticker
        """
        retval = {}


        # First find all matches in the submission title and add them to the return value
        for phrase in re.findall(self.ticker_re, submission.title):
            if phrase not in self.blacklist and phrase in tickers:
                if retval.get(phrase):
                    retval[phrase]["mentions"] = retval.get('mentions',[]).append({"location": "submission", "id": submission.id})
                    retval[phrase]["count"] = retval.get(phrase).get("count", 0) + 1
                else:
                    retval[phrase] = {
                        "mentions": [{"location": "submission", "id": submission.id}],
                        "count": 1
                    }

        # load all the comments
        # replace more with a limit of 0 will ensure that we get all the comments
        # even from long threads
        comments = await submission.comments()
        await comments.replace_more(limit=0)

        # count the matches in every comment
        coros = [self._get_comment_tickers(c, tickers) async for c in comments]
        results = await asyncio.gather(*coros)

        # results will be a list of coroutine returns which is a list of dictionaries in the format:
        #     [
        #       { "MSFT": {
        #           "location": "comment",
        #           "id": "ad83nh",
        #           "count": 3
        #         }
        #        }
        #        ...
        #      ]
        #
        # Need to add all of these dicts into a single dict

        for result in results:
            for symbol, details in result.items():
                if retval.get(symbol):
                    #symbol has already been created in return value, so need to combine
                    retval[symbol]["mentions"] += details.get("mentions", [])
                    retval[symbol]["count"] += details.get("count")
                else:
                    #symbol has not already been created, so create it
                    retval[symbol] = {
                        "mentions": details.get("mentions", []),
                        "count": details.get("count")
                    }

        return retval



    async def _get_subreddit_tickers(self, subreddit: asyncpraw.models.Subreddit, tickers: List[str]) -> Dict[str, int]:
        """
        Parses the top posts for a subreddit for the current day and counts the number of times a regular expression occurs

        Args:
            subreddit (asyncpraw.subreddit): Subreddit to parse
            tickers (List[str]): list of stock tickers to check against

        Returns:
            Dict[str, int]: Dictionary with count of occurences for each ticker
        """
        submissions = subreddit.top("day")
        coros = [self._get_submission_tickers(s, tickers) async for s in submissions]

        results = await asyncio.gather(*coros)


        retval = {}

        for result in results:
            for symbol, details in result.items():
                if retval.get(symbol):
                    #symbol has already been created in return value, so need to combine
                    retval[symbol]["mentions"] += details.get("mentions", [])
                    retval[symbol]["count"] += details.get("count")
                else:
                    #symbol has not already been created, so create it
                    retval[symbol] = {
                        "mentions": details.get("mentions", []),
                        "count": details.get("count")
                    }

        # Combine list of dicts returned from all runs
        return retval

    async def get_top_tickers(self, subreddit: str, tickers: List[str]) -> Dict[str, int]:
        """
        Retrieves the top mentioned strings from the tickers list in a given subreddit on the current day

        Args:
            subreddit (str): subreddit to search
            tickers (List[str]): list of strings to match

        Returns:
            Dict[str, int]: Dictionary with count of occurences per match
        """
        sub = await self.reddit.subreddit(subreddit)
        return await self._get_subreddit_tickers(sub, tickers)


# async def get_ticker_mentions(subreddit: str, tickers: List[str]):
#     """""
#     Searches a subreddit to retrieve the top tickers mentioned

#     Args:
#         subreddit (str): subreddit to scrape
#         tickers (List[str]): list of tickers to search for

#     Returns:
#         [type]: [description]
#     """
#     ssl_ctx = ssl._create_unverified_context()

#     conn = aiohttp.TCPConnector(ssl_context=ssl_ctx)
#     session = aiohttp.ClientSession(connector=conn)
#     reddit = asyncpraw.Reddit(
#         client_id=settings.REDDIT_CLIENT_ID,
#         client_secret=settings.REDDIT_CLIENT_SECRET,
#         user_agent="YoloFund",
#         requestor_kwargs={"session": session},
#     )
#     dailyTickers = {}

#     regexPattern = r'\b([A-Z]+)\b'
#     blacklist = 
#     sub = await reddit.subreddit(subreddit)

#     async for submission in sub.top("day"):
#         print(submission)
#         strings = [submission.title]
#         comments = await submission.comments()
#         await comments.replace_more(limit=0)
#         async for comment in comments:
#             strings.append(comment.body)
#         for s in strings:
#             for phrase in re.findall(regexPattern, s):
#                 if phrase not in blacklist:
#                     if phrase in tickers:
#                         dailyTickers[phrase] = dailyTickers.get(phrase, 0) + 1

#     return dailyTickers


#     return True