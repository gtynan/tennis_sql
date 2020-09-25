from typing import Optional, Union
from pydantic import BaseModel as Base, validator
import numpy as np


class BaseModel(Base):
    id: Optional[Union[str, int]]

    class Config:
        orm_mode = True


class CreateModel(Base):

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
