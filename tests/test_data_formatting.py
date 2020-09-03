import pytest
from datetime import datetime

from src.data_formatting import format_player
from src.db.models.player import Player


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
