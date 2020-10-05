from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from .base import Base
from .performance import WPerformance, LPerformance


class Game(Base):
    """SQL alchemy table structure for Game
    """
    __tablename__ = 'game'

    id = Column(String(50), primary_key=True)

    round = Column(String(50))
    score = Column(String(50))
    match_num = Column(Integer)

    tournament_id = Column(String(50), ForeignKey('tournament.id'))
    tournament = relationship("Tournament", uselist=False, foreign_keys=[tournament_id], back_populates="games")

    w_performance = relationship("WPerformance", uselist=False)
    l_performance = relationship("LPerformance", uselist=False)
