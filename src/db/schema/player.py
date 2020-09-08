from typing import List
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .base import BaseTable, BaseModel
from .performance import PerformanceSchema


class PlayerTable(BaseTable):
    """SQL alchemy table structure for Player
    """
    __tablename__ = 'player'

    first_name = Column(String(50))
    last_name = Column(String(50))
    nationality = Column(String(50))
    dob = Column(DateTime)
    hand = Column(String(50))

    performances = relationship("_PerformanceTable", back_populates='player')

    @hybrid_property
    def name(self):
        return self.first_name + " " + self.last_name


class PlayerBaseSchema(BaseModel):
    """Pydantic base schema for player
    """
    first_name: str
    last_name: str
    nationality: str
    dob: datetime
    hand: str

    class Config:
        orm_mode = True


class PlayerCreateSchema(PlayerBaseSchema):
    """Pydantic create schema for player
    """
    pass


class PlayerSchema(PlayerBaseSchema):
    """Pydantic object schema for player
    """
    id: int
    name: str
    performances: List[PerformanceSchema] = []
