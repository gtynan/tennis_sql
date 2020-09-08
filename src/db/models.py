from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

from ..constants import WTA_IDENTIFIER, ITF_IDENTIFIER

Base = declarative_base()


class TableBase(Base):
    '''Ensures all tables in our db have an id col in their schema
    '''
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Player(TableBase):
    __tablename__ = 'player'

    first_name = Column(String(50))
    last_name = Column(String(50))
    nationality = Column(String(50))
    dob = Column(DateTime)
    hand = Column(String(50))

    # one player has many performances
    # cascade all delete ensure when a player is deleted so is all their performances (helps with teardown of db)
    # performances = relationship("Performance", backref='player', cascade="all, delete")

    @hybrid_property
    def name(self):
        return self.first_name + " " + self.last_name


class Tournament(TableBase):
    __tablename__ = 'tournament'

    name = Column(String(50))
    surface = Column(String(50))
    draw_size = Column(Integer)
    level = Column(String(50))
    start_date = Column(DateTime)
