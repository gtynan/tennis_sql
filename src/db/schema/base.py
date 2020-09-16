from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy import Column, Integer
from pydantic import BaseModel, validator
import numpy as np

Base: DeclarativeMeta = declarative_base()


class BaseTable(Base):
    """SQL Alchemy abstract base table to ensure all tables have an id column
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class CreateModel(BaseModel):

    @validator('*')
    def nan_to_none(cls, v, field):
        """pandas nan values when passed to string columns are converted literally via pydantic to 'nan', 
           float nan values are also not accepted. This function ensures they are given None values and thus NULL in db
        """
        if (field.outer_type_ is str and v == 'nan') | (field.outer_type_ is float and np.isnan(v)):
            return None
        return v

    # allows comparisons via np.unique()
    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id
