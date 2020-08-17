from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Player(Base):
    '''
    Table map based on: https://github.com/JeffSackmann/tennis_wta/blob/master/wta_players.csv
    '''
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)

    fname = Column(String(50))
    lname = Column(String(50))
    nationality = Column(String(3))
    dob = Column(Date)
    hand = Column(String(1))
