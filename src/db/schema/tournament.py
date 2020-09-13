from typing import List
from datetime import datetime

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

from .base import BaseTable, BaseModel


class TournamentTable(BaseTable):
    """SQL alchemy table structure for Tournament
    """
    __tablename__ = 'tournament'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    surface = Column(String(50))
    draw_size = Column(Integer)
    level = Column(String(50))
    start_date = Column(DateTime)


class TournamentBaseSchema(BaseModel):
    """Pydantic base schema for tournaments
    """
    id: str
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
    pass
