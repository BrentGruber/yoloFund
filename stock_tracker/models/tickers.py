from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

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
    symbol = fields.CharField(max_length=16, index=True)
    type = fields.CharField(max_length=64, index=True)

Ticker_Pydantic = pydantic_model_creator(Ticker, name="Ticker")
TickerIn_Pydantic = pydantic_model_creator(Ticker, name="TickerIn", exclude_readonly=True)
