from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Float
from sqlalchemy.orm import relationship

from .base import BaseTable, BaseModel
from .player import PlayerSchema


class _PerformanceTable(BaseTable):
    """SQL alchemy table structure for Performance (SHOULD NEVER BE DIRECTLY INSTANCIATED USE CHILD)
    """
    __tablename__ = 'performance'

    # player who's performance it relates to
    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship("PlayerTable", uselist=False, foreign_keys=player_id)

    # player game stats
    aces = Column(Float)
    double_faults = Column(Float)
    serve_points = Column(Float)
    first_serve_in = Column(Float)
    first_serve_won = Column(Float)
    second_serve_won = Column(Float)
    serve_games = Column(Float)
    break_points_faced = Column(Float)
    break_points_saved = Column(Float)

    # outcome
    won = Column(Boolean, nullable=False)

    __mapper_args__ = {
        'polymorphic_on': won,
    }


class WPerformanceTable(_PerformanceTable):
    """SQL alchemy table structure for winning performance 
    """
    __tablename__ = 'w_performance'

    id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

    # game winning performance relates to
    game_id = Column(String(50), ForeignKey('game.id'))
    game = relationship("GameTable", back_populates="w_performance", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': True  # won = True
    }


class LPerformanceTable(_PerformanceTable):
    """SQL alchemy table structure for losing performance 
    """
    __tablename__ = 'l_performance'

    id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

    # game losing performance relates to
    game_id = Column(String(50), ForeignKey('game.id'))
    game = relationship("GameTable", back_populates="l_performance", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': False  # won = False
    }


class PerformanceBaseSchema(BaseModel):
    """Pydantic base schema for performances
    """
    aces: float
    double_faults: float
    serve_points: float
    first_serve_in: float
    first_serve_won: float
    second_serve_won: float
    serve_games: float
    break_points_faced: float
    break_points_saved: float


class PerformanceCreateSchema(PerformanceBaseSchema):
    """Pydantic create schema for performances
    """
    game_id: str
    player_id: int
    # used in db.py add_performance() to determine which table to insert to
    won: bool


class PerformanceSchema(PerformanceBaseSchema):
    """Pydantic object schema for performances
    """
    player: PlayerSchema

    class Config:
        orm_mode = True
