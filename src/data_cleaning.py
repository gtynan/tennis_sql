from typing import Tuple, Union
import pandas as pd
import numpy as np
from datetime import datetime
import re

from .db.tables import Player, _Game, WTA, ITF, Tournament
from .constants import player_csv_map, game_csv_map, tournament_csv_map


def raw_player_to_object(raw_player: pd.Series) -> Player:
    return Player(id=raw_player[player_csv_map['id']],
                  fname=raw_player[player_csv_map['fname']],
                  lname=raw_player[player_csv_map['lname']],
                  nationality=raw_player[player_csv_map['nationality']],
                  dob=datetime.strptime(
                      str(raw_player[player_csv_map['dob']]), '%Y%m%d'),
                  hand=raw_player[player_csv_map['hand']])


def raw_game_to_object(raw_game: pd.Series) -> Union[WTA, ITF]:
    w_games, w_sets, l_games, l_sets = score_to_int_data(
        raw_game[game_csv_map['score']])

    game = _Game(
        round=raw_game[game_csv_map['round']],
        score=raw_game[game_csv_map['score']],
        w_player_id=raw_game[game_csv_map['w_player_id']],
        w_games=w_games,
        w_sets=w_sets,
        w_rank=raw_game[game_csv_map['w_rank']],
        l_player_id=raw_game[game_csv_map['l_player_id']],
        l_games=l_games,
        l_sets=l_sets,
        l_rank=raw_game[game_csv_map['l_rank']],
        completed=~pd.isnull(w_sets)
    )
    # casting to child based on source
    if raw_game['source'] == 'W':
        game.__class__ = WTA
    else:
        game.__class__ = ITF
    return game


def raw_tournament_to_object(raw_tournament: pd.Series) -> Tournament:
    return Tournament(
        name=raw_tournament[tournament_csv_map['name']],
        start_date=datetime.strptime(
            raw_tournament[tournament_csv_map['start_date']], '%Y%m%d'),
        surface=raw_tournament[tournament_csv_map['surface']],
        level=raw_tournament[tournament_csv_map['level']]
    )


def score_to_int_data(score: str) -> Tuple[int, int, int, int]:
    '''
    Converts string score to int values representing games and sets won by winner and loser

    args:
        score: string score

    returns:
        WGames, WSets, LGames, LSets
    '''
    if pd.isnull(score):
        return -1

    # regex to remove brackets and the contnets within
    score = re.sub(r'\([^)]*\)', '', score).strip()
    set_score = score.split(' ')

    try:
        # must be at least 2 sets
        assert len(set_score) >= 2
        game_score = np.array([set_score_.split('-')
                               for set_score_ in set_score], dtype=int)
        # winner must win at least 12 games
        assert game_score[:, 0].sum() >= 12
    except:
        return np.NaN  #  triggered if string in score ie W/O or RET or assertions not met
    return game_score[:, 0].sum(), 2, game_score[:, 1].sum(), len(set_score) - 2
