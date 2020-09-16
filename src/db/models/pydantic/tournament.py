from datetime import datetime

from .base import BaseModel, CreateModel


class TournamentBase(BaseModel):
    """Pydantic base schema for tournaments
    """
    id: str
    name: str
    surface: str
    draw_size: int
    level: str
    start_date: datetime


class TournamentCreate(TournamentBase, CreateModel):
    """Pydantic create schema for tournaments
    """
    pass


class Tournament(TournamentBase):
    """Pydantic object schema for tournaments
    """
    pass
