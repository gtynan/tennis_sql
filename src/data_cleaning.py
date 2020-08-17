from typing import Tuple
import pandas as pd
import numpy as np
from datetime import datetime
import re

from .db.tables import Player
from .constants import player_csv_map


def raw_player_to_object(raw_player: pd.Series) -> Player:
    return Player(fname=raw_player[player_csv_map['fname']],
                  lname=raw_player[player_csv_map['lname']],
                  nationality=raw_player[player_csv_map['nationality']],
                  dob=datetime.strptime(
                      str(raw_player[player_csv_map['dob']]), '%Y%m%d'),
                  hand=raw_player[player_csv_map['hand']])


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
