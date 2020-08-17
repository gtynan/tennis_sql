import pandas as pd
from datetime import datetime

from src.data_cleaning import raw_player_to_object
from src.constants import player_csv_map


def test_raw_player_to_object():
    fname, lname, nationality, dob, hand = "Tom", "Robinson", "USA", "20000101", "R"

    raw_player = pd.Series(data=[fname, lname, nationality, dob, hand],
                           index=player_csv_map.values())

    player_object = raw_player_to_object(raw_player)

    assert player_object.fname == fname
    assert player_object.lname == lname
    assert player_object.nationality == nationality
    assert player_object.dob == datetime.strptime(dob, '%Y%m%d')
    assert player_object.hand == hand
