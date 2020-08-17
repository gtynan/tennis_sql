import pandas as pd
from datetime import datetime

from .db.tables import Player
from .constants import player_csv_map


def raw_player_to_object(raw_player: pd.Series) -> Player:
    return Player(fname=raw_player[player_csv_map['fname']],
                  lname=raw_player[player_csv_map['lname']],
                  nationality=raw_player[player_csv_map['nationality']],
                  dob=datetime.strptime(
                      raw_player[player_csv_map['dob']], '%Y%m%d'),
                  hand=raw_player[player_csv_map['hand']])
