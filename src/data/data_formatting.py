from typing import Tuple, Iterator
import pandas as pd

from ..constants import SOURCE_COL
from .data_cleaning import to_datetime, get_game_id
from ..db.models.pydantic.player import PlayerCreate
from ..db.models.pydantic.tournament import TournamentCreate
from ..db.models.pydantic.game import GameCreate
from ..db.models.pydantic.performance import PerformanceCreate


def format_player(row: pd.Series, id: str = '200000', fname: str = 'X', lname: str = 'X.1', nationality: str = 'UNK', dob: str = '19000000', hand: str = 'U') -> PlayerCreate:
    """
    """
    return PlayerCreate(
        id=row[id],
        first_name=row[fname],
        last_name=row[lname],
        nationality=row[nationality],
        dob=to_datetime(row[dob]),
        hand=row[hand])


def raw_game_to_instances(row: pd.Series) -> Tuple[TournamentCreate, GameCreate, PerformanceCreate, PerformanceCreate]:
    """
    """
    tournament = format_tournament(row)
    game = format_game(row)
    w_performance, l_performance = format_performances(row, game.id)
    return tournament, game, w_performance, l_performance


def format_tournament(row: object, id: str = 'tourney_id', name: str = 'tourney_name', surface: str = 'surface', draw_size: str = 'draw_size', level: str = 'tourney_level', start_date: str = 'tourney_date') -> TournamentCreate:
    """
    """
    return TournamentCreate(id=row[id],
                            name=row[name],
                            surface=row[surface],
                            draw_size=row[draw_size],
                            level=row[level],
                            start_date=to_datetime(row[start_date]))


def format_game(row: pd.Series, tournament_id: str = 'tourney_id', match_num: str = 'match_num', round: str = 'round', score: str = 'score', circuit: str = SOURCE_COL) -> GameCreate:
    """
    """
    return GameCreate(id=get_game_id(row[tournament_id], row[match_num]),
                      tournament_id=row[tournament_id],
                      round=row[round],
                      score=row[score],
                      circuit=row[circuit])


def format_performances(row: pd.Series,  game_id: str,  player_id: str = 'id', aces: str = 'ace', double_faults: str = 'df',
                        serve_points: str = 'svpt', f_serve_in: str = '1stIn', f_serve_won: str = '1stWon', s_serve_won: str = '2ndWon', serve_games: str = 'SvGms', b_points_faced: str = 'bpFaced',
                        b_points_saved: str = 'bpSaved', w_prefix: str = 'w_', l_prefix: str = 'l_') -> Iterator[PerformanceCreate]:
    """
    """
    for prefix, outcome in [(w_prefix, True), (l_prefix, False)]:
        yield PerformanceCreate(game_id=game_id,
                                player_id=row[prefix + player_id],
                                won=outcome,
                                aces=row[prefix + aces],
                                double_faults=row[prefix + double_faults],
                                serve_points=row[prefix + serve_points],
                                first_serve_in=row[prefix + f_serve_in],
                                first_serve_won=row[prefix + f_serve_won],
                                second_serve_won=row[prefix + s_serve_won],
                                serve_games=row[prefix + serve_games],
                                break_points_faced=row[prefix + b_points_faced],
                                break_points_saved=row[prefix + b_points_saved])
