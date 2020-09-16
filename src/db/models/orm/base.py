from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer

SQLAlchemyBase: DeclarativeMeta = declarative_base()


class Base(SQLAlchemyBase):
    """SQL Alchemy abstract base table to ensure all tables have an id column
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
