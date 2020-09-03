import pytest
from datetime import datetime
from inspect import signature

from src.data_formatting import format_player, format_tournament, format_game, _format_performance
from src.db.models.player import Player
from src.db.models.tournament import Tournament
from src.db.models.game import WTA, ITF
from src.constants import SOURCE_COL


@pytest.mark.slow
def test_format_player(sample_players):
    player = format_player(sample_players.iloc[0])

    assert isinstance(player, Player)
    assert player.first_name == sample_players.loc[0, 'X']
    assert player.last_name == sample_players.loc[0, 'X.1']
    assert player.nationality == sample_players.loc[0, 'UNK']
    # convert back to int to ensure date correctly mapped
    assert int(player.dob.strftime('%Y%m%d')) == sample_players.loc[0, '19000000']
    assert isinstance(player.dob, datetime)
    assert player.hand == sample_players.loc[0, 'U']


@pytest.mark.slow
def test_format_tournament(sample_games):
    tournament = format_tournament(sample_games.iloc[0])

    assert isinstance(tournament, Tournament)
    assert tournament.name == sample_games.loc[0, 'tourney_name']
    assert tournament.surface == sample_games.loc[0, 'surface']
    assert tournament.draw_size == sample_games.loc[0, 'draw_size']
    assert tournament.level == sample_games.loc[0, 'tourney_level']
    assert int(tournament.start_date.strftime('%Y%m%d')) == sample_games.loc[0, 'tourney_date']
    assert isinstance(tournament.start_date, datetime)


@pytest.mark.slow
def test_format_game(sample_players, sample_games):
    print(sample_games)
    w_player, l_player = format_player(sample_players.iloc[0]), format_player(sample_players.iloc[1])
    sample_game = sample_games.iloc[0]
    tournament = format_tournament(sample_game)

    game = format_game(sample_game, tournament, w_player, l_player)

    assert isinstance(game, WTA)
    assert game.tournament == tournament
    assert game.round == sample_game['round']
    assert game.score == sample_game['score']

    assert game.w_performance.player == w_player
    assert game.l_performance.player == l_player

    # getting default args from function to ensure matches with expected params
    # ie order matches with _format_performance order
    performance_cols = signature(format_game).parameters['performance_cols'].default

    for (prefix, performance) in [('w_', game.w_performance), ('l_', game.l_performance)]:
        cols = [prefix+col for col in performance_cols]

        assert performance.aces == sample_game[cols[0]]
        assert performance.double_faults == sample_game[cols[1]]
        assert performance.serve_points == sample_game[cols[2]]
        assert performance.first_serve_in == sample_game[cols[3]]
        assert performance.first_serve_won == sample_game[cols[4]]
        assert performance.second_serve_won == sample_game[cols[5]]
        assert performance.serve_games == sample_game[cols[6]]
        assert performance.break_points_faced == sample_game[cols[7]]
        assert performance.break_points_saved == sample_game[cols[8]]

    # ensuring if source changes function casts to new source
    sample_game[SOURCE_COL] = 'I'
    game = format_game(sample_game, tournament, w_player, l_player)
    assert isinstance(game, ITF)


@pytest.mark.slow
def test_format_performance(sample_players, sample_games):
    player = format_player(sample_players.iloc[0])
    game = sample_games.iloc[0]

    performance = _format_performance(game, player, 'w_ace', 'w_df', 'w_svpt', 'w_1stIn',
                                      'w_1stWon', 'w_2ndWon', 'w_SvGms', 'w_bpFaced', 'w_bpSaved')

    assert performance.player == player
    assert performance.aces == game['w_ace']
    assert performance.double_faults == game['w_df']
    assert performance.serve_points == game['w_svpt']
    assert performance.first_serve_in == game['w_1stIn']
    assert performance.first_serve_won == game['w_1stWon']
    assert performance.second_serve_won == game['w_2ndWon']
    assert performance.break_points_faced == game['w_bpFaced']
    assert performance.break_points_saved == game['w_bpSaved']
