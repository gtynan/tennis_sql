from typing import Tuple, List
import pandas as pd
from datetime import datetime

from .constants import SOURCE_COL
from .db.models.player import Player
from .db.models.tournament import Tournament
from .db.models.performance import Performance
from .db.models.game import _Game, WTA, ITF


def format_player(row: object, fname: str = 'X', lname: str = 'X.1', nationality: str = 'UNK', dob: str = '19000000', hand: str = 'U') -> Player:
    """Given row from jeff sackmans player csv formats to player object

    Args:
        row (object): DataFrame row 
        fname (str, optional): column containing first name. Defaults to 'X'.
        lname (str, optional): column containing last name. Defaults to 'X.1'.
        nationality (str, optional): column containing nationality. Defaults to 'UNK'.
        dob (str, optional): column containing date of birth. Defaults to '19000000'.
        hand (str, optional): column containing hand. Defaults to 'U'.

    Returns:
        Player: player instance
    """
    return Player(first_name=row[fname],
                  last_name=row[lname],
                  nationality=row[nationality],
                  dob=datetime.strptime(str(row[dob]), '%Y%m%d'),
                  hand=row[hand])


def format_tournament(row: object, name: str = 'tourney_name', surface: str = 'surface', draw_size: str = 'draw_size', level: str = 'tourney_level', start_date: str = 'tourney_date') -> Tournament:
    """Given row from jeff sackmans matches csv formats to tournament object

    Args:
        row (object): DataFrame row
        name (str, optional): column containing tournament name. Defaults to 'tourney_name'.
        surface (str, optional): column containing surface type. Defaults to 'surface'.
        draw_size (str, optional): column containing draw size. Defaults to 'draw_size'.
        level (str, optional): column containing tournament level. Defaults to 'tourney_level'.
        start_date (str, optional): column containing tournament start date. Defaults to 'tourney_date'.

    Returns:
        Tournament: tournament instance
    """
    return Tournament(name=row[name],
                      surface=row[surface],
                      draw_size=row[draw_size],
                      level=row[level],
                      start_date=datetime.strptime(str(row[start_date]), '%Y%m%d'))


def format_game(row: object, tournament: Tournament, w_player: Player, l_player: Player, source: str = SOURCE_COL, round: str = 'round', score: str = 'score',
                performance_cols: List[str] = ['ace', 'df', 'svpt', '1stIn', '1stWon', '2ndWon', 'SvGms', 'bpFaced', 'bpSaved'],
                w_prefix: str = 'w_', l_prefix: str = 'l_') -> _Game:
    """Given row from jeff sackmans matches csv formats to game object

    Args:
        row (object): DataFrame row
        tournament (Tournament): tournament instance in row
        w_player (Player): winning player instance in row
        l_player (Player): losing player instance in row
        source (str, optional): column denoting circuit source (W = WTA, I = ITF). Defaults to SOURCE_COL.
        round (str, optional): column containing match round. Defaults to 'round'.
        score (str, optional): column containing match score. Defaults to 'score'.
        performance_cols (List[str], optional): list of columns relating to performance (sans prefix) should match _format_performance order. Defaults to ['ace', 'df', 'svpt', '1stIn', '1stWon', '2ndWon', 'SvGms', 'bpFaced', 'bpSaved'].
        w_prefix (str, optional): winning player prefix on performance cols. Defaults to 'w_'.
        l_prefix (str, optional): losing player prefix on performance cols. Defaults to 'l_'.

    Returns:
        _Game: game instance of row
    """

    w_performance = _format_performance(row, w_player, *[w_prefix + col for col in performance_cols])
    l_performance = _format_performance(row, l_player, *[l_prefix + col for col in performance_cols])

    game = WTA(round=row[round],
               score=row[score],
               tournament=tournament,
               w_performance=w_performance,
               l_performance=l_performance)

    # cast to ITF
    if row[source] != 'W':
        game.__class__ = ITF
        game.circuit = ITF.__mapper_args__['polymorphic_identity']

    return game


def _format_performance(row: object, player: Player,  aces: str, double_faults: str, serve_points: str,
                        f_serve_in: str, f_serve_won: str, s_serve_won: str, serve_games: str, b_points_faced: str,
                        b_points_saved: str) -> Performance:
    """Should only be called by format_game as performances do not have a uniqueness and are only relevant relating to a game
    """
    return Performance(aces=row[aces],
                       double_faults=row[double_faults],
                       serve_points=row[serve_points],
                       first_serve_in=row[f_serve_in],
                       first_serve_won=row[f_serve_won],
                       second_serve_won=row[s_serve_won],
                       serve_games=row[serve_games],
                       break_points_faced=row[b_points_faced],
                       break_points_saved=row[b_points_saved],
                       player=player)
