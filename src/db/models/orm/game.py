from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base
from .performance import WPerformance, LPerformance


class Game(Base):
    """SQL alchemy table structure for Game
    """
    __tablename__ = 'game'

    id = Column(String(50), primary_key=True)

    tournament_id = Column(String(50), ForeignKey('tournament.id'))
    tournament = relationship("Tournament", uselist=False, foreign_keys=[tournament_id])

    w_performance = relationship("WPerformance", uselist=False)
    l_performance = relationship("LPerformance", uselist=False)

    round = Column(String(50))
    score = Column(String(50))
