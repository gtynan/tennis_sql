from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer

SQLAlchemyBase: DeclarativeMeta = declarative_base()


class Base(SQLAlchemyBase):
    """SQL Alchemy custom base table to ensure all tables have an id column
    """
    id = Column(Integer, primary_key=True, autoincrement=True)


Base = declarative_base(cls=Base)
