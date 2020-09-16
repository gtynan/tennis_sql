from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, Float
from sqlalchemy.orm import relationship

from .base import Base


class _Performance(Base):
    """SQL alchemy table structure for Performance (SHOULD NEVER BE DIRECTLY INSTANCIATED USE CHILD)
    """
    __tablename__ = 'performance'

    # player who's performance it relates to
    player_id = Column(Integer, ForeignKey("player.id"))
    player = relationship("Player", uselist=False, foreign_keys=player_id)

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


class WPerformance(_Performance):
    """SQL alchemy table structure for winning performance 
    """
    __tablename__ = 'w_performance'

    id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

    # game winning performance relates to
    game_id = Column(String(50), ForeignKey('game.id'))
    game = relationship("Game", back_populates="w_performance", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': True  # won = True
    }


class LPerformance(_Performance):
    """SQL alchemy table structure for losing performance 
    """
    __tablename__ = 'l_performance'

    id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

    # game losing performance relates to
    game_id = Column(String(50), ForeignKey('game.id'))
    game = relationship("Game", back_populates="l_performance", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': False  # won = False
    }
