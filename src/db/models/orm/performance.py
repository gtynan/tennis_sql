from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .base import Base


class PerformanceMixin:
    """Mixin to declare shared attributes between winning and losing performance
    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

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

    @declared_attr
    def player_id(cls):
        # player who's performance it relates to
        return Column(Integer, ForeignKey("player.id"))

    @declared_attr
    def player(cls):
        return relationship("Player", uselist=False)


class WPerformance(PerformanceMixin, Base):
    """SQL alchemy table structure for winning performance 
    """
    id = Column(Integer, primary_key=True)

    # game winning performance relates to
    game_id = Column(String(50), ForeignKey('game.id'))
    game = relationship("Game", back_populates="w_performance", uselist=False)


class LPerformance(PerformanceMixin, Base):
    """SQL alchemy table structure for losing performance 
    """
    id = Column(Integer, primary_key=True)

    # game losing performance relates to
    game_id = Column(String(50), ForeignKey('game.id'))
    game = relationship("Game", back_populates="l_performance", uselist=False)
