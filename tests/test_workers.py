import pytest

from src.db.db import CommandDB, QueryDB
from src.db.models.orm.player import Player
from src.db.models.orm.tournament import Tournament
from src.db.models.orm.game import Game
from src.db.models.orm.performance import WPerformance, LPerformance
from src.workers import add_player_data, add_game_data
from src.data.data_cleaning import get_game_id


@pytest.fixture(scope='module')
def command_db(db_client):
    return CommandDB(db_client.session)


@pytest.mark.slow
def test_add_player_data(command_db, sample_players):
    add_player_data(command_db, sample_players, bulk=True)

    # ensure all players added
    for _, player in sample_players.iterrows():
        command_db.session.query(Player).\
            filter(Player.id == player['200000']).one()


@pytest.mark.slow
def test_add_game_data(command_db, sample_games, sample_players):
    # when adding performance will back check player_id thus needs to already be ingested
    # by setting the id's = to player_id's already ingested we ensure no errors
    sample_games['winner_id'] = sample_players['200000'].values
    sample_games['loser_id'] = sample_players['200000'].values

    add_game_data(command_db, sample_games, bulk=True)

    # ensure all objects added
    for _, game_row in sample_games.iterrows():
        game_id = get_game_id(game_row['tourney_id'], game_row['match_num'])

        # check all tables that should have a reference to this game_row
        command_db.session.query(Tournament).\
            filter(Tournament.id == game_row['tourney_id']).one()
        command_db.session.query(Game).\
            filter(Game.id == game_id).one()
        command_db.session.query(WPerformance).\
            filter(WPerformance.game_id == game_id).one()
        command_db.session.query(LPerformance).\
            filter(LPerformance.game_id == game_id).one()
