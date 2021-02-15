from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

from .exchanges import Exchange

class Ticker(models.Model):
    """
    The Ticker model
    """
    id = fields.IntField(pk=True)
    currency = fields.CharField(max_length=8, index=True)
    description = fields.CharField(max_length=255)
    displaySymbol = fields.CharField(max_length=16, index=True)
    figi = fields.CharField(max_length=32)
    mic = fields.CharField(max_length=32)
    symbol = fields.CharField(max_length=16, index=True, unique=True)
    type = fields.CharField(max_length=64, index=True)
    exchange: fields.ForeignKeyRelation[Exchange] = fields.ForeignKeyField(
        "models.Exchange", related_name="tickers"
    )

Ticker_Pydantic = pydantic_model_creator(Ticker, name="Ticker")
TickerIn_Pydantic = pydantic_model_creator(Ticker, name="TickerIn", exclude_readonly=True)
