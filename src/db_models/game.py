from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import BASE
from .tournament import Tournament
from .performance import Performance


class _Game(BASE):
    __tablename__ = 'game'

    id = Column(Integer, primary_key=True, autoincrement=True)

    tournament_id = Column(Integer, ForeignKey(f'{Tournament.__tablename__}.id'))
    round = Column(String(50))
    score = Column(String(50))

    w_performance_id = Column(Integer, ForeignKey(f'{Performance.__tablename__}.id'))
    l_performance_id = Column(Integer, ForeignKey(f'{Performance.__tablename__}.id'))

    tournament = relationship("Tournament", foreign_keys=[tournament_id])
    w_performance = relationship("Performance", foreign_keys=[w_performance_id])
    l_performance = relationship("Performance", foreign_keys=[l_performance_id])

    type = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'game',
        'polymorphic_on': type
    }


class WTA(_Game):
    __tablename__ = 'wta'

    id = Column(Integer, ForeignKey(f'{_Game.__tablename__}.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'wta',
    }


class ITF(_Game):
    __tablename__ = 'itf'

    id = Column(Integer, ForeignKey(f'{_Game.__tablename__}.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'itf',
    }
