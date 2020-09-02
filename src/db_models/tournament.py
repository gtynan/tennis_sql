from sqlalchemy import Column, Integer, String, Date
from .base import BASE


class Tournament(BASE):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    surface = Column(String(50))
    draw_size = Column(Integer)
    level = Column(String(50))
    start_date = Column(Date)
