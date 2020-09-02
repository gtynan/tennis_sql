from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import BASE
from .player import Player


class Performance(BASE):
    __tablename__ = 'performance'

    id = Column(Integer, primary_key=True, autoincrement=True)

    player_id = Column(Integer, ForeignKey(f'{Player.__tablename__}.id'))
    seed = Column(Integer)
    entry = Column(String(50))
    aces = Column(Integer)
    double_faults = Column(Integer)
    serve_points = Column(Integer)
    first_serve_in = Column(Integer)
    first_serve_won = Column(Integer)
    second_serve_won = Column(Integer)
    serve_games = Column(Integer)
    break_points_faced = Column(Integer)
    break_points_saved = Column(Integer)
    player_rank = Column(Integer)
    player_points = Column(Integer)

    player = relationship("Player", foreign_keys=[player_id])
