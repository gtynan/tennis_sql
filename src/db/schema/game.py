from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import BaseTable, BaseModel, CreateModel
from .player import PlayerSchema
from .performance import PerformanceSchema
from .tournament import TournamentSchema


class GameTable(BaseTable):
    """SQL alchemy table structure for Game
    """
    __tablename__ = 'game'

    id = Column(String(50), primary_key=True)

    tournament_id = Column(String(50), ForeignKey('tournament.id'))
    tournament = relationship("TournamentTable", uselist=False, foreign_keys=[tournament_id])

    w_performance = relationship("WPerformanceTable", uselist=False)
    l_performance = relationship("LPerformanceTable", uselist=False)

    round = Column(String(50))
    score = Column(String(50))
    circuit = Column(String(50))


class GameBaseSchema(BaseModel):
    """Pydantic base schema for games
    """
    id: str
    round: str
    score: Optional[str] = None
    circuit: str

    class Config:
        orm_mode = True


class GameCreateSchema(GameBaseSchema, CreateModel):
    """Pydantic create schema for games
    """
    tournament_id: str


class GameSchema(GameBaseSchema):
    """Pydantic object schema for games
    """
    tournament: TournamentSchema
    # must leave optional as performance added after game and thus
    # theoretically possible game could be queried before performance added
    w_performance: Optional[PerformanceSchema] = None
    l_performance: Optional[PerformanceSchema] = None
