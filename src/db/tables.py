from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Player(Base):
    '''
    Table schema based on: https://github.com/JeffSackmann/tennis_wta/blob/master/wta_players.csv
    '''
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True, autoincrement=True)

    fname = Column(String(50))
    lname = Column(String(50))
    nationality = Column(String(3))
    dob = Column(Date)
    hand = Column(String(1))


class _Game(Base):
    '''
    Base game table (should never be written to directly)
    '''
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)

    tournament_id = Column(Integer, ForeignKey('tournament.id'))
    round = Column(String(20))
    score = Column(String(20))

    w_player_id = Column(Integer, ForeignKey('player.id'))
    w_games = Column(Integer)
    w_sets = Column(Integer)
    w_rank = Column(Integer)

    l_player_id = Column(Integer, ForeignKey('player.id'))
    l_games = Column(Integer)
    l_sets = Column(Integer)
    l_rank = Column(Integer)

    completed = Column(Boolean)
    type = Column(String(4))

    tournament = relationship("Tournament", foreign_keys=[tournament_id])
    w_player = relationship("Player", foreign_keys=[w_player_id])
    l_player = relationship("Player", foreign_keys=[l_player_id])

    __mapper_args__ = {
        'polymorphic_identity': 'game',
        'polymorphic_on': type
    }


class WTA(_Game):
    __tablename__ = 'wta'

    id = Column(Integer, ForeignKey('game.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'WTA',
    }


class ITF(_Game):
    __tablename__ = 'itf'

    id = Column(Integer, ForeignKey('game.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'ITF',
    }


class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    start_date = Column(Date)
    surface = Column(String(10))
    level = Column(String(1))
