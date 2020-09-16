import pytest
from datetime import datetime

from src.data.data_formatting import format_player, format_tournament, format_game, format_performances, raw_game_to_instances

from src.db.models.pydantic.player import PlayerCreate
from src.db.models.pydantic.game import GameCreate
from src.db.models.pydantic.tournament import TournamentCreate
from src.db.models.pydantic.performance import PerformanceCreate


@pytest.mark.slow
def test_format_player(sample_players):
    player = format_player(sample_players.iloc[0])

    assert isinstance(player, PlayerCreate)
    assert player.id == sample_players.loc[0, '200000']
    assert player.first_name == sample_players.loc[0, 'X']
    assert player.last_name == sample_players.loc[0, 'X.1']
    assert player.nationality == sample_players.loc[0, 'UNK']
    # convert back to int to ensure date correctly mapped
    assert int(player.dob.strftime('%Y%m%d')) == sample_players.loc[0, '19000000']
    assert isinstance(player.dob, datetime)
    assert player.hand == sample_players.loc[0, 'U']


@pytest.mark.slow
def test_raw_game_to_instances(sample_games):
    game = sample_games.iloc[0].rename({'winner_id': 'w_id', 'loser_id': 'l_id'})

    tournament, game, w_perf, l_perf = raw_game_to_instances(game)
    assert isinstance(tournament, TournamentCreate)
    assert isinstance(game, GameCreate)
    assert isinstance(w_perf, PerformanceCreate)
    assert isinstance(l_perf, PerformanceCreate)


@pytest.mark.slow
def test_format_tournament(sample_games):
    tournament = format_tournament(sample_games.iloc[0])

    assert isinstance(tournament, TournamentCreate)
    assert tournament.id == sample_games.loc[0, 'tourney_id']
    assert tournament.name == sample_games.loc[0, 'tourney_name']
    assert tournament.surface == sample_games.loc[0, 'surface']
    assert tournament.draw_size == sample_games.loc[0, 'draw_size']
    assert tournament.level == sample_games.loc[0, 'tourney_level']
    assert int(tournament.start_date.strftime('%Y%m%d')) == sample_games.loc[0, 'tourney_date']
    assert isinstance(tournament.start_date, datetime)


@pytest.mark.slow
def test_format_game(sample_games):
    game = format_game(sample_games.iloc[0])

    assert isinstance(game, GameCreate)
    assert game.tournament_id == sample_games.loc[0, 'tourney_id']
    assert game.id == f"{sample_games.loc[0, 'tourney_id']}_{sample_games.loc[0, 'match_num']}"
    assert game.round == sample_games.loc[0, 'round']
    assert game.score == sample_games.loc[0, 'score']


@pytest.mark.slow
def test_format_performances(sample_games):
    game = sample_games.iloc[0].rename({'winner_id': 'w_id', 'loser_id': 'l_id'})

    w_perf, l_perf = format_performances(game, 'test_game')

    assert w_perf.game_id == l_perf.game_id == 'test_game'

    assert isinstance(w_perf, PerformanceCreate)
    assert isinstance(l_perf, PerformanceCreate)

    assert w_perf.player_id == game['w_id']
    assert w_perf.won
    assert w_perf.aces == game['w_ace']
    assert w_perf.double_faults == game['w_df']
    assert w_perf.serve_points == game['w_svpt']
    assert w_perf.first_serve_in == game['w_1stIn']
    assert w_perf.first_serve_won == game['w_1stWon']
    assert w_perf.second_serve_won == game['w_2ndWon']
    assert w_perf.break_points_faced == game['w_bpFaced']
    assert w_perf.break_points_saved == game['w_bpSaved']

    assert l_perf.player_id == game['l_id']
    assert ~l_perf.won
    assert l_perf.aces == game['l_ace']
    assert l_perf.double_faults == game['l_df']
    assert l_perf.serve_points == game['l_svpt']
    assert l_perf.first_serve_in == game['l_1stIn']
    assert l_perf.first_serve_won == game['l_1stWon']
    assert l_perf.second_serve_won == game['l_2ndWon']
    assert l_perf.break_points_faced == game['l_bpFaced']
    assert l_perf.break_points_saved == game['l_bpSaved']
