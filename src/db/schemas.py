from datetime import datetime
from pydantic import BaseModel


class GameBase(BaseModel):
    tournament: Tournament
    round: str
    score: str
    w_performance: Performance
    l_performance: Performance


class GameCreate(GameBase):
    pass


class Game:
    id: int
    tournament_id: int
    w_performance_id: int
    l_performance_id: int


class PerformanceBase(BaseModel):
    aces: int
    double_faults: int
    serve_points: int
    first_serve_in: int
    first_serve_won: int
    second_serve_won: int
    serve_games: int
    break_points_faced: int
    break_points_saved: int
    player: Player


class PerformanceCreate(PerformanceBase):
    pass


class Performance(PerformanceBase):
    id: int
    player_id: int


class PlayerBase(BaseModel):
    first_name: str
    last_name: str
    nationality: str
    dob: datetime
    hand: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    name: str

    class Config:
        orm_mode = True


class TournamentBase(BaseModel):
    name: str
    surface: str
    draw_size: int
    level: str
    start_date: datetime


class TournamentCreate(TournamentBase):
    pass


class Tournament(TournamentBase):
    id: int

    class Config:
        orm_mode = True
