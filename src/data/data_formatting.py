from typing import Tuple, Iterator
import pandas as pd

from ..constants import SOURCE_COL, PLAYER_COLS, GAME_COLS, TOURNAMENT_COLS, PERFORMANCE_COLS
from .data_cleaning import to_datetime
from ..db.models.pydantic.player import PlayerCreate
from ..db.models.pydantic.tournament import TournamentCreate
from ..db.models.pydantic.game import GameCreate
from ..db.models.pydantic.performance import PerformanceCreate


def format_player(row: pd.Series) -> PlayerCreate:
    """Converts row in Jeff Sackmans players csv to a pydantic create object

    Args:
        row (pd.Series): player row

    Returns:
        PlayerCreate: pydantic create object
    """
    return PlayerCreate(
        id=row[PLAYER_COLS['id']],
        first_name=row[PLAYER_COLS['first_name']],
        last_name=row[PLAYER_COLS['last_name']],
        nationality=row[PLAYER_COLS['nationality']],
        dob=to_datetime(row[PLAYER_COLS['dob']]),
        hand=row[PLAYER_COLS['hand']])


def raw_game_to_objects(row: pd.Series) -> Tuple[TournamentCreate, GameCreate, PerformanceCreate, PerformanceCreate]:
    """Given a game row from Jeff Sackmans game csv convert to pydantic db create objects 

    Args:
        row (pd.Series): game row

    Returns:
        Tuple[TournamentCreate, GameCreate, PerformanceCreate, PerformanceCreate]: DB objects to describe game
    """
    tournament = _format_tournament(row)
    game = _format_game(row)
    w_performance, l_performance = _format_performances(row, game.id)
    return tournament, game, w_performance, l_performance


def _format_tournament(row: pd.Series) -> TournamentCreate:
    """Create pydantic tournament create object from game row 
    """
    return TournamentCreate(id=row[TOURNAMENT_COLS['id']],
                            name=row[TOURNAMENT_COLS['name']],
                            surface=row[TOURNAMENT_COLS['surface']],
                            draw_size=row[TOURNAMENT_COLS['draw_size']],
                            level=row[TOURNAMENT_COLS['level']],
                            start_date=to_datetime(row[TOURNAMENT_COLS['start_date']]),
                            circuit=row[TOURNAMENT_COLS['circuit']])


def _format_game(row: pd.Series) -> GameCreate:
    """Create pydantic game create object from game row 
    """
    return GameCreate(tournament_id=row[GAME_COLS['tournament_id']],
                      match_num=row[GAME_COLS['match_num']],
                      round=row[GAME_COLS['round']],
                      score=row[GAME_COLS['score']])


def _format_performances(row: pd.Series,  game_id: str) -> Iterator[PerformanceCreate]:
    """Create pydantic winning and losing performances create objects from game row 
    """
    for prefix, outcome in [('w_', True), ('l_', False)]:
        yield PerformanceCreate(game_id=game_id,
                                player_id=row[prefix + PERFORMANCE_COLS['player_id']],
                                won=outcome,
                                aces=row[prefix + PERFORMANCE_COLS['aces']],
                                double_faults=row[prefix + PERFORMANCE_COLS['double_faults']],
                                serve_points=row[prefix + PERFORMANCE_COLS['serve_points']],
                                first_serve_in=row[prefix + PERFORMANCE_COLS['first_serve_in']],
                                first_serve_won=row[prefix + PERFORMANCE_COLS['first_serve_won']],
                                second_serve_won=row[prefix + PERFORMANCE_COLS['second_serve_won']],
                                serve_games=row[prefix + PERFORMANCE_COLS['serve_games']],
                                break_points_faced=row[prefix + PERFORMANCE_COLS['break_points_faced']],
                                break_points_saved=row[prefix + PERFORMANCE_COLS['break_points_saved']])
