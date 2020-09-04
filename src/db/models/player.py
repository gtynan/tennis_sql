from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.hybrid import hybrid_property
from .base import BASE


class Player(BASE):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)

    first_name = Column(String(50))
    last_name = Column(String(50))
    nationality = Column(String(50))
    dob = Column(Date)
    hand = Column(String(50))

    @hybrid_property
    def name(self):
        return self.first_name + " " + self.last_name
