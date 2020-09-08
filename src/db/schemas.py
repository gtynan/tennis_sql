from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    nationality: str
    dob: datetime
    hand: str

    # allow us to use from_orm for tests
    # would be in Player class if not for tests so doesn't matter as would be used anyway
    class Config:
        orm_mode = True


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    name: str
