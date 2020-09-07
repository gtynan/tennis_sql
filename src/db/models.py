from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class _Game(Base):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)

    tournament_id = Column(Integer, ForeignKey(f'tournament.id'))
    round = Column(String(50))
    score = Column(String(50))

    w_performance_id = Column(Integer, ForeignKey(f'performance.id'))
    l_performance_id = Column(Integer, ForeignKey(f'performance.id'))

    tournament = relationship("Tournament", foreign_keys=[tournament_id])
    w_performance = relationship("Performance", foreign_keys=[w_performance_id])
    l_performance = relationship("Performance", foreign_keys=[l_performance_id])

    circuit = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'game',
        'polymorphic_on': circuit
    }


class WTA(_Game):
    __tablename__ = 'wta'

    id = Column(Integer, ForeignKey(f'game.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'wta',
    }


class ITF(_Game):
    __tablename__ = 'itf'

    id = Column(Integer, ForeignKey(f'game.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'itf',
    }


class Performance(Base):
    __tablename__ = 'performance'

    id = Column(Integer, primary_key=True, autoincrement=True)

    player_id = Column(Integer, ForeignKey(f'player.id'))

    aces = Column(Integer)
    double_faults = Column(Integer)
    serve_points = Column(Integer)
    first_serve_in = Column(Integer)
    first_serve_won = Column(Integer)
    second_serve_won = Column(Integer)
    serve_games = Column(Integer)
    break_points_faced = Column(Integer)
    break_points_saved = Column(Integer)

    player = relationship("Player", foreign_keys=[player_id])


class Player(Base):
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


class Tournament(Base):
    __tablename__ = 'tournament'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    surface = Column(String(50))
    draw_size = Column(Integer)
    level = Column(String(50))
    start_date = Column(Date)
