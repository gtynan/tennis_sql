from typing import Tuple, Iterator
import pandas as pd

from ..constants import SOURCE_COL
from .data_cleaning import to_datetime, get_game_id
from ..db.models.pydantic.player import PlayerCreate
from ..db.models.pydantic.tournament import TournamentCreate
from ..db.models.pydantic.game import GameCreate
from ..db.models.pydantic.performance import PerformanceCreate


def format_player(row: pd.Series, id: str = '200000', fname: str = 'X', lname: str = 'X.1', nationality: str = 'UNK', dob: str = '19000000', hand: str = 'U') -> PlayerCreate:
    """Converts row in Jeff Sackmans players csv to a pydantic create object

    Args:
        row (pd.Series): player row
        id (str, optional): player id column. Defaults to '200000'.
        fname (str, optional): player first name column. Defaults to 'X'.
        lname (str, optional): player last name column. Defaults to 'X.1'.
        nationality (str, optional): player nationality column. Defaults to 'UNK'.
        dob (str, optional): player date of birth column. Defaults to '19000000'.
        hand (str, optional): player hand column. Defaults to 'U'.

    Returns:
        PlayerCreate: pydantic create object
    """
    return PlayerCreate(
        id=row[id],
        first_name=row[fname],
        last_name=row[lname],
        nationality=row[nationality],
        dob=to_datetime(row[dob]),
        hand=row[hand])


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


def _format_tournament(row: pd.Series, id: str = 'tourney_id', name: str = 'tourney_name', surface: str = 'surface', draw_size: str = 'draw_size', level: str = 'tourney_level', start_date: str = 'tourney_date', circuit: str = SOURCE_COL) -> TournamentCreate:
    """Create pydantic tournament create object from game row 
    """
    return TournamentCreate(id=row[id],
                            name=row[name],
                            surface=row[surface],
                            draw_size=row[draw_size],
                            level=row[level],
                            start_date=to_datetime(row[start_date]),
                            circuit=row[circuit])


def _format_game(row: pd.Series, tournament_id: str = 'tourney_id', match_num: str = 'match_num', round: str = 'round', score: str = 'score', circuit: str = SOURCE_COL) -> GameCreate:
    """Create pydantic game create object from game row 
    """
    return GameCreate(  # id=get_game_id(row[tournament_id], row[match_num]),
        tournament_id=row[tournament_id],
        match_num=row[match_num],
        round=row[round],
        score=row[score])


def _format_performances(row: pd.Series,  game_id: str,  player_id: str = 'id', aces: str = 'ace', double_faults: str = 'df',
                         serve_points: str = 'svpt', f_serve_in: str = '1stIn', f_serve_won: str = '1stWon', s_serve_won: str = '2ndWon', serve_games: str = 'SvGms', b_points_faced: str = 'bpFaced',
                         b_points_saved: str = 'bpSaved', w_prefix: str = 'w_', l_prefix: str = 'l_') -> Iterator[PerformanceCreate]:
    """Create pydantic winning and losing performances create objects from game row 
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
