from typing import Optional
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import BaseTable, BaseModel
from .player import PlayerSchema
from .performance import PerformanceSchema
from .tournament import TournamentSchema


class GameTable(BaseTable):
    """SQL alchemy table structure for Game
    """
    __tablename__ = 'game'

    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship("TournamentTable", uselist=False, foreign_keys=[tournament_id])

    w_performance = relationship("WPerformanceTable", uselist=False)
    l_performance = relationship("LPerformanceTable", uselist=False)

    round = Column(String(50))
    score = Column(String(50))
    circuit = Column(String(50))


class GameBaseSchema(BaseModel):
    """Pydantic base schema for games
    """
    round: str
    score: str
    circuit: str

    class Config:
        orm_mode = True


class GameCreateSchema(GameBaseSchema):
    """Pydantic create schema for games
    """
    tournament_id: int


class GameSchema(GameBaseSchema):
    """Pydantic object schema for games
    """
    id: int
    tournament: TournamentSchema
    # must leave optional as performance added after game and thus
    # theoretically possible game could be queried before performance added
    w_performance: Optional[PerformanceSchema] = None
    l_performance: Optional[PerformanceSchema] = None
