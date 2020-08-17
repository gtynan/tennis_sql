import pandas as pd
import numpy as np
from datetime import datetime

from src.db.tables import WTA
from src.data.data_cleaning import (
    raw_player_to_object, raw_game_to_object, raw_tournament_to_object, score_to_int_data)
from src.constants import player_csv_map, game_csv_map, tournament_csv_map


def test_raw_player_to_object():
    id, fname, lname, nationality, dob, hand = 1, "Tom", "Robinson", "USA", 20000101, "R"

    raw_player = pd.Series(data=[id, fname, lname, nationality, dob, hand],
                           index=player_csv_map.values())
    player_object = raw_player_to_object(raw_player)

    assert player_object.fname == fname
    assert player_object.lname == lname
    assert player_object.nationality == nationality
    assert player_object.dob == datetime.strptime(str(dob), '%Y%m%d')
    assert player_object.hand == hand


def test_raw_game_to_object():
    round_, score, w_id, w_rank, l_id, l_rank, source = 'SF', '6-0 6-2', 1, 1, 2, 2, 'W'

    raw_game = pd.Series(data=[round_, score, w_id, w_rank, l_id, l_rank, source],
                         index=list(game_csv_map.values()) + ['source'])
    game_object = raw_game_to_object(raw_game)

    assert isinstance(game_object, WTA)
    assert game_object.round == round_
    assert game_object.score == score
    assert game_object.w_player_id == w_id
    assert game_object.w_games == 12
    assert game_object.w_sets == 2
    assert game_object.w_rank == w_rank
    assert game_object.l_player_id == l_id
    assert game_object.l_games == 2
    assert game_object.l_sets == 0
    assert game_object.l_rank == l_rank


def test_raw_tournament_to_object():
    name, start_date, surface, level = "Auckland", "20200101", "Grass", "PM"

    raw_tournament = pd.Series(data=[name, start_date, surface, level],
                               index=tournament_csv_map.values())
    tournament_object = raw_tournament_to_object(raw_tournament)

    assert tournament_object.name == name
    assert tournament_object.start_date == datetime.strptime(
        start_date, '%Y%m%d')
    assert tournament_object.surface == surface
    assert tournament_object.level == level


def test_score_to_int_data():
    # (Wgames, Wsets, Lgames, Lsets)
    assert score_to_int_data('7-6(7) 6-0') == (13, 2, 6, 0)
    # ensure invalid scores are handled
    assert np.isnan(score_to_int_data('6-0 RET'))
    assert np.isnan(score_to_int_data('6-0'))
    assert np.isnan(score_to_int_data('1-0 1-0'))
    # nan scores are handled by the model and denoted as -1
    assert score_to_int_data(np.NaN) == -1
