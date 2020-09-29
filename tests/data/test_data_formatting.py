import pytest
from datetime import datetime

from src.data.data_formatting import format_player, _format_tournament, _format_game, _format_performances, raw_game_to_objects

from src.db.models.pydantic.player import PlayerCreate
from src.db.models.pydantic.game import GameCreate
from src.db.models.pydantic.tournament import TournamentCreate
from src.db.models.pydantic.performance import PerformanceCreate

from src.constants import PLAYER_COLS, TOURNAMENT_COLS, GAME_COLS, PERFORMANCE_COLS


@pytest.mark.slow
def test_format_player(sample_players):
    sample_player = sample_players.iloc[0]
    formatted_player = format_player(sample_player).dict()

    # check formatted values match to original values
    for db_col, j_col in PLAYER_COLS.items():
        # we expect dob to be converted to datetime
        if db_col == 'dob':
            assert isinstance(formatted_player[db_col], datetime)
            assert int(formatted_player[db_col].strftime('%Y%m%d')) == sample_player[j_col]
        else:
            assert formatted_player[db_col] == sample_player[j_col]


@pytest.mark.slow
def test_raw_game_to_objects(sample_games):
    sample_game = sample_games.iloc[0].rename({'winner_id': 'w_id', 'loser_id': 'l_id'})

    tournament, game, w_perf, l_perf = raw_game_to_objects(sample_game)
    assert isinstance(tournament, TournamentCreate)
    assert isinstance(game, GameCreate)
    assert isinstance(w_perf, PerformanceCreate)
    assert isinstance(l_perf, PerformanceCreate)


@pytest.mark.slow
def test_format_tournament(sample_games):
    sample_game = sample_games.iloc[0]
    formatted_tournament = _format_tournament(sample_game).dict()

    # check formatted values match to original values
    for db_col, j_col in TOURNAMENT_COLS.items():
        # we expect start_date to be converted to datetime
        if db_col == 'start_date':
            assert isinstance(formatted_tournament[db_col], datetime)
            assert int(formatted_tournament[db_col].strftime('%Y%m%d')) == sample_game[j_col]
        else:
            assert formatted_tournament[db_col] == sample_game[j_col]


@pytest.mark.slow
def test_format_game(sample_games):
    sample_game = sample_games.iloc[0]
    formatted_game = _format_game(sample_game).dict()

    # ensure id correctly generated from __init__ function
    assert formatted_game['id'] == f"{sample_game[GAME_COLS['tournament_id']]}_{sample_game[GAME_COLS['match_num']]}"

    # check formatted values match to original values
    for db_col, j_col in GAME_COLS.items():
        assert formatted_game[db_col] == sample_game[j_col]


@pytest.mark.slow
def test_format_performances(sample_games):
    sample_game = sample_games.iloc[0].rename({'winner_id': 'w_id', 'loser_id': 'l_id'})

    formatted_w_perf, formatted_l_perf = [perf.dict() for perf in _format_performances(sample_game, 'test_game')]

    assert formatted_w_perf['game_id'] == formatted_l_perf['game_id'] == 'test_game'

    # check formatted values match to original values
    for prefix, performance in [('w_', formatted_w_perf), ('l_', formatted_l_perf)]:
        for db_col, j_col in PERFORMANCE_COLS.items():
            assert performance[db_col] == sample_game[prefix + j_col]  # have to add prefix back

    # ensure outcomes as expected
    assert formatted_w_perf['won']
    assert ~formatted_l_perf['won']
