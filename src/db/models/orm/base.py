from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer


class _Base:
    """SQL Alchemy custom base table to ensure all tables have an id column
    """
    id = Column(Integer, primary_key=True, autoincrement=True)


Base: DeclarativeMeta = declarative_base(cls=_Base)
