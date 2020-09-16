from typing import Optional

from .base import BaseModel, CreateModel
from .performance import Performance
from .tournament import Tournament


class GameBase(BaseModel):
    """Pydantic base schema for games
    """
    id: str
    round: str
    score: Optional[str] = None
    circuit: str


class GameCreate(GameBase, CreateModel):
    """Pydantic create schema for games
    """
    tournament_id: str


class Game(GameBase):
    """Pydantic object schema for games
    """
    tournament: Tournament
    # must leave optional as performance added after game and thus
    # theoretically possible game could be queried before performance added
    w_performance: Optional[Performance] = None
    l_performance: Optional[Performance] = None
