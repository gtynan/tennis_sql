from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from .base import Base


class Tournament(Base):
    """SQL alchemy table structure for Tournament
    """
    __tablename__ = 'tournament'

    id = Column(String(50), primary_key=True)
    name = Column(String(100))
    surface = Column(String(50))
    draw_size = Column(Integer)
    level = Column(String(50))
    start_date = Column(DateTime)
    circuit = Column(String(50))

    games = relationship("Game", uselist=True)
