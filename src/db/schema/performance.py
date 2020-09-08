from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import BaseTable, BaseModel


class _PerformanceTable(BaseTable):
    """SQL alchemy table structure for Performance (SHOULD NEVER BE DIRECTLY INSTANCIATED USE CHILD)
    """
    __tablename__ = 'performance'

    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("PlayerTable", back_populates="performances", uselist=False)

    aces = Column(Integer)
    double_faults = Column(Integer)
    serve_points = Column(Integer)
    first_serve_in = Column(Integer)
    first_serve_won = Column(Integer)
    second_serve_won = Column(Integer)
    serve_games = Column(Integer)
    break_points_faced = Column(Integer)
    break_points_saved = Column(Integer)

    won = Column(Boolean, nullable=False)

    __mapper_args__ = {
        'polymorphic_on': won,
    }


class WPerformanceTable(_PerformanceTable):
    """SQL alchemy table structure for winning performance 
    """
    __tablename__ = 'w_performance'

    id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

    # game has a winning and losing performance hence need to create child performances
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("GameTable", back_populates="w_performance", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': True  # won = True
    }


class LPerformanceTable(_PerformanceTable):
    """SQL alchemy table structure for losing performance 
    """
    __tablename__ = 'l_performance'

    id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

    # game has a winning and losing performance hence need to create child performances
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("GameTable", back_populates="l_performance", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': False  # won = False
    }


class PerformanceBaseSchema(BaseModel):
    """Pydantic base schema for performances
    """
    won: bool

    aces: Optional[int]
    double_faults: Optional[int]
    serve_points: Optional[int]
    first_serve_in: Optional[int]
    first_serve_won: Optional[int]
    second_serve_won: Optional[int]
    serve_games: Optional[int]
    break_points_faced: Optional[int]
    break_points_saved: Optional[int]


class PerformanceCreateSchema(PerformanceBaseSchema):
    """Pydantic create schema for performances
    """
    pass


class PerformanceSchema(PerformanceBaseSchema):
    """Pydantic object schema for performances
    """
    id: int
    player_id: int
    game_id: int

    class Config:
        orm_mode = True
