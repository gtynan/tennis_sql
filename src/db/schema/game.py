from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from.base import BaseTable, BaseModel


class GameTable(BaseTable):
    """SQL alchemy table structure for Game
    """
    __tablename__ = 'game'

    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship("TournamentTable", back_populates='games', uselist=False)

    w_performance = relationship("WPerformanceTable", back_populates='game', uselist=False)
    l_performance = relationship("LPerformanceTable", back_populates='game', uselist=False)

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
    pass


class GameSchema(GameBaseSchema):
    """Pydantic object schema for games
    """
    id: int
    tournament_id: int
