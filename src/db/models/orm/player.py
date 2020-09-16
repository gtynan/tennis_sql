from sqlalchemy import Column, String, DateTime

from .base import Base


class Player(Base):
    """SQL alchemy table structure for Player
    """
    __tablename__ = 'player'

    first_name = Column(String(50))
    last_name = Column(String(50))
    nationality = Column(String(50))
    dob = Column(DateTime)
    hand = Column(String(50), default='U')
