import pandas as pd
import numpy as np
from datetime import datetime

from src.data_cleaning import raw_player_to_object, score_to_int_data
from src.constants import player_csv_map


def test_raw_player_to_object():
    fname, lname, nationality, dob, hand = "Tom", "Robinson", "USA", 20000101, "R"

    raw_player = pd.Series(data=[fname, lname, nationality, dob, hand],
                           index=player_csv_map.values())

    player_object = raw_player_to_object(raw_player)

    assert player_object.fname == fname
    assert player_object.lname == lname
    assert player_object.nationality == nationality
    assert player_object.dob == datetime.strptime(str(dob), '%Y%m%d')
    assert player_object.hand == hand


def test_score_to_int_data():
    # (Wgames, Wsets, Lgames, Lsets)
    assert score_to_int_data('7-6(7) 6-0') == (13, 2, 6, 0)
    # ensure invalid scores are handled
    assert np.isnan(score_to_int_data('6-0 RET'))
    assert np.isnan(score_to_int_data('6-0'))
    assert np.isnan(score_to_int_data('1-0 1-0'))
    # nan scores are handled by the model and denoted as -1
    assert score_to_int_data(np.NaN) == -1
