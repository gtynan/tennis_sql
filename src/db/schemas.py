from typing import Optional, List
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


class GameBase(BaseModel):
    round: str
    score: str
    circuit: str

    class Config:
        orm_mode = True


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    tournament_id: int


class TournamentBase(BaseModel):
    name: str
    surface: str
    draw_size: int
    level: str
    start_date: datetime

    class Config:
        orm_mode = True


class TournamentCreate(TournamentBase):
    pass


class Tournament(TournamentBase):
    id: int
    games: List[Game]


class PerformanceBase(BaseModel):
    won: bool


class PerformanceCreate(PerformanceBase):
    pass


class Performance(PerformanceBase):
    id: int
    player_id: int
    game_id: int

    class Config:
        orm_mode = True
