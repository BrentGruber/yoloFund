from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

class Exchange(models.Model):
    """
    The Exchange model
    """
    id = fields.IntField(pk=True)
    code = fields.CharField(max_length=8, unique=True)
    name = fields.CharField(max_length=128, index=True)
    mic = fields.CharField(max_length=16)
    timezone = fields.CharField(max_length=64, index=True)
    open_time = fields.CharField(max_length=32, index=True)
    country = fields.CharField(max_length=8, index=True)
    source = fields.TextField()

Exchange_Pydantic = pydantic_model_creator(Exchange, name="Exchange")
ExchangeIn_Pydantic = pydantic_model_creator(Exchange, name="ExchangeIn", exclude_readonly=True)