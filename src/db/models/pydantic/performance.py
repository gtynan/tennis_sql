from typing import Optional

from .base import BaseModel, CreateModel
from .player import Player


class PerformanceBase(BaseModel):
    """Pydantic base schema for performances
    """
    aces: Optional[float]
    double_faults: Optional[float]
    serve_points: Optional[float]
    first_serve_in: Optional[float]
    first_serve_won: Optional[float]
    second_serve_won: Optional[float]
    serve_games: Optional[float]
    break_points_faced: Optional[float]
    break_points_saved: Optional[float]


class PerformanceCreate(PerformanceBase, CreateModel):
    """Pydantic create schema for performances
    """
    game_id: str
    player_id: int
    # used in db.py add_performance() to determine which table to insert to
    won: bool

    # override CreateModel comprison
    def __eq__(self, other):
        return (self.game_id == other.game_id) and (self.won == other.won)

    def __lt__(self, other):
        return (self.game_id < other.game_id) or (self.game_id == other.game_id and self.won < other.won)


class Performance(PerformanceBase):
    """Pydantic object schema for performances
    """
    player: Player
