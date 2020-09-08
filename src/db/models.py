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
    '''
    One player has many performances
    '''

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


# class _Game(Base):
#     '''
#     one game has one tournament, one winning performance and one losing performance
#     '''
#     __tablename__ = 'game'

#     id = Column(Integer, primary_key=True, autoincrement=True)

#     tournament_id = Column(Integer, ForeignKey(f'tournament.id'), nullable=False)
#     tournament = relationship("Tournament", backref='games', foreign_keys=[tournament_id])

#     # # w_performance_id = Column(Integer, ForeignKey(f'performance.id'))
#     # w_performance = relationship("Performance",  uselist=False, back_populates='game')

#     # # l_performance_id = Column(Integer, ForeignKey(f'performance.id'))
#     # l_performance = relationship("Performance",  uselist=False, back_populates='game')

#     round = Column(String(50))
#     score = Column(String(50))

#     circuit = Column(String(50))

#     __mapper_args__ = {
#         'polymorphic_identity': 'game',
#         'polymorphic_on': circuit
#     }


# class Tournament(Base):
#     '''
#     One tournament has many games
#     '''
#     __tablename__ = 'tournament'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     surface = Column(String(50))
#     draw_size = Column(Integer)
#     level = Column(String(50))
#     start_date = Column(DateTime)


# class WTA(_Game):
#     __tablename__ = 'wta'

#     id = Column(Integer, ForeignKey(f'game.id'), primary_key=True)

#     __mapper_args__ = {
#         'polymorphic_identity': WTA_IDENTIFIER,
#     }


# class ITF(_Game):
#     __tablename__ = 'itf'

#     id = Column(Integer, ForeignKey(f'game.id'), primary_key=True)

#     __mapper_args__ = {
#         'polymorphic_identity': ITF_IDENTIFIER,
#     }


# class Player(Base):
#     '''
#     One player has many performances
#     '''

#     __tablename__ = 'player'

#     id = Column(Integer, primary_key=True, autoincrement=True)

#     first_name = Column(String(50))
#     last_name = Column(String(50))
#     nationality = Column(String(50))
#     dob = Column(DateTime)
#     hand = Column(String(50))

#     # one player has many performances
#     # cascade all delete ensure when a player is deleted so is all their performances (helps with teardown of db)
#     performances = relationship("Performance", backref='player', cascade="all, delete")

#     @hybrid_property
#     def name(self):
#         return self.first_name + " " + self.last_name


# class Performance(Base):
#     '''
#     One performance has one player and one game
#     '''
#     __tablename__ = 'performance'

#     id = Column(Integer, primary_key=True, autoincrement=True)

#     # one performance has one player
#     player_id = Column(Integer, ForeignKey(f'player.id'), nullable=False)
#     # player = relationship("Player", back_populates="performances")

#     aces = Column(Integer)
#     double_faults = Column(Integer)
#     serve_points = Column(Integer)
#     first_serve_in = Column(Integer)
#     first_serve_won = Column(Integer)
#     second_serve_won = Column(Integer)
#     serve_games = Column(Integer)
#     break_points_faced = Column(Integer)
#     break_points_saved = Column(Integer)
#     won = Column(Boolean)

#     __mapper_args__ = {
#         'polymorphic_identity': False,
#         'polymorphic_on': won
#     }


# class WPerformance(Performance):
#     __tablename__ = 'w_performance'

#     id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

#     __mapper_args__ = {
#         'polymorphic_identity': True,
#     }


# class LPerformance(Performance):
#     __tablename__ = 'l_performance'

#     id = Column(Integer, ForeignKey(f'performance.id'), primary_key=True)

#     __mapper_args__ = {
#         'polymorphic_identity': False,
#     }
