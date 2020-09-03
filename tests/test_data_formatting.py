import pytest
from datetime import datetime

from src.data_formatting import format_player, format_tournament
from src.db.models.player import Player
from src.db.models.tournament import Tournament


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
