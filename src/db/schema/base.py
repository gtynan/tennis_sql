from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer
from pydantic import BaseModel

Base: DeclarativeMeta = declarative_base()


class BaseTable(Base):
    """SQL Alchemy abstract base table to ensure all tables have an id column
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
