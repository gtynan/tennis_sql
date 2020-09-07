import pytest
from datetime import datetime
from src.data_cleaning import to_datetime
from src.data_ingestion import add_games
from src.data_formatting import format_player
from src.db.db import CommandDB, QueryDB
from src.db.models import WTA

# TODO expand tests


@pytest.mark.slow
def test_add_games(db_client, sample_players, sample_games):
    w_player, l_player = format_player(sample_players.iloc[0]), format_player(sample_players.iloc[1])

    sample_game = sample_games.iloc[0].copy(deep=True)

    t_date = to_datetime(sample_game['tourney_date'])
    # add_game queries these columns to match players so adjusting data to match our two formatted players
    sample_game['winner_name'] = w_player.name
    sample_game['winner_age'] = (t_date - w_player.dob).days/365.24

    sample_game['loser_name'] = l_player.name
    sample_game['loser_age'] = (t_date - l_player.dob).days/365.24

    command_db = CommandDB(db_client.session)
    command_db.add_player(w_player)
    command_db.add_player(l_player)

    add_games(db_client.session, sample_game)

    query_db = QueryDB(db_client.session)
    tournament = query_db.get_tournament(sample_game['tourney_name'], t_date)
    game = query_db.get_game(tournament, w_player, l_player)

    assert isinstance(game, WTA)
