from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from .tickers import Ticker

class TickerMentions(models.Model):
    """
    The Ticker model
    """
    id = fields.IntField(pk=True)
    date = fields.DateField(index=True)
    ticker: fields.ForeignKeyRelation[Ticker] = fields.ForeignKeyField(
        "models.Ticker", related_name="mentions"
    )
    count = fields.IntegerField()
    mentions = fields.JSONField()

TickerMentions_Pydantic = pydantic_model_creator(TickerMentions, name="TickerMentions")
TickerMentionsIn_Pydantic = pydantic_model_creator(TickerMentions, name="TickerMentionsIn", exclude_readonly=True)