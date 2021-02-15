from pydantic import BaseModel
from typing import Dict


class StringMatch(BaseModel):
    """
    Object used to contain information about regex matches in a reddit entity
    """
    count: int = Field(...)
    location: str = Field(...)
    reddit_id: str = Field(...)

class TickerMatchCreate(BaseModel):
    """
    Object used for ticker matches
    """
    __root__: Dict[str, Type[StringMatch]]