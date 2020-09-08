from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from .base import BaseTable, BaseModel


class TournamentTable(BaseTable):
    """SQL alchemy table structure for Tournament
    """
    __tablename__ = 'tournament'

    name = Column(String(50))
    surface = Column(String(50))
    draw_size = Column(Integer)
    level = Column(String(50))
    start_date = Column(DateTime)

    games = relationship("GameTable", back_populates='tournament')


class TournamentBaseSchema(BaseModel):
    """Pydantic base schema for tournaments
    """
    name: str
    surface: str
    draw_size: int
    level: str
    start_date: datetime

    class Config:
        orm_mode = True


class TournamentCreateSchema(TournamentBaseSchema):
    """Pydantic create schema for tournaments
    """
    pass


class TournamentSchema(TournamentBaseSchema):
    """Pydantic object schema for tournaments
    """
    id: int
    games: List[Game] = []
