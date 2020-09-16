from typing import Optional
from datetime import datetime

from .base import BaseModel, CreateModel


class PlayerBase(BaseModel):
    """Pydantic base schema for player
    """
    id: int
    first_name: str
    last_name: str
    nationality: str
    dob: Optional[datetime] = None
    hand: str


class PlayerCreate(PlayerBase, CreateModel):
    """Pydantic create schema for player
    """
    pass


class Player(PlayerBase):
    """Pydantic object schema for player
    """
    pass
