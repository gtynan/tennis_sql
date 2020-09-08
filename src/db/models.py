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

    w_performances = relationship("WPerformance", back_populates='player')
    l_performances = relationship("LPerformance", back_populates='player')

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

    games = relationship("Game", back_populates='tournament')


class Game(TableBase):
    __tablename__ = 'game'

    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    tournament = relationship("Tournament", back_populates='games')

    w_performance = relationship("WPerformance", back_populates='game', uselist=False)
    l_performance = relationship("LPerformance", back_populates='game', uselist=False)

    round = Column(String(50))
    score = Column(String(50))
    circuit = Column(String(50))


class Performance(TableBase):
    __abstract__ = True
    # TODO all performances cols ie ACE
    won = Column(Boolean)


class WPerformance(Performance):
    __tablename__ = 'w_performance'

    # ideally would be in performance table but can't have relationship in abstract class
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("Player", back_populates="w_performances")

    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("Game", back_populates="w_performance")


class LPerformance(Performance):
    __tablename__ = 'l_performance'

    # ideally would be in performance table but can't have relationship in abstract class
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship("Player", back_populates="l_performances")

    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship("Game", back_populates="l_performance")
