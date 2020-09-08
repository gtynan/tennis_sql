import pytest
import datetime
import numpy as np

from ..conftest import TEST_DB
from src.db.db import CommandDB, DBClient
from src.db import models  # import Player, Tournament, Performance, WTA, ITF

from src.db import schemas  # import PlayerCreate
from src.constants import WTA_IDENTIFIER


@pytest.fixture(scope='module')
def sample_player() -> models.Player:
    return models.Player(first_name='Tom', last_name='Jones', nationality='IRE', dob=datetime.datetime(2000, 1, 1), hand='R')


@pytest.fixture(scope='module')
def sample_tournament() -> models.Tournament:
    return models.Tournament(name='Aus Open', surface='Hard', draw_size=32, level='G', start_date=datetime.datetime(2000, 1, 1))


class TestDBClient:

    def test_init(self, db_client: DBClient):
        '''
        Ensure connected to expected database.
        '''
        assert db_client.engine.url.database == TEST_DB


class TestCommandDB:

    @pytest.fixture(scope='class')
    def command_db(self, db_client) -> CommandDB:
        return CommandDB(db_client.session)

    def test_add_player(self, db_client, command_db, sample_player):
        # convert to pydantic object to validate insert schema
        player = schemas.PlayerCreate.from_orm(sample_player)
        # function being tested
        player_id = command_db.add_player(player)

        # retrieve added player from db
        queried_player = db_client.session.query(models.Player).\
            filter(models.Player.id == player_id).one()
        # ensure matches expected schema (will raise exception otherwise)
        schemas.Player.from_orm(queried_player)

        assert queried_player.first_name == player.first_name
        assert queried_player.last_name == player.last_name
        assert queried_player.nationality == player.nationality
        assert queried_player.dob == player.dob
        assert queried_player.hand == player.hand
        assert queried_player.name == player.first_name + " " + player.last_name

    def test_add_tournament(self, db_client, command_db, sample_tournament):
        # convert to pydantic object to validate insert schema
        tournament = schemas.TournamentCreate.from_orm(sample_tournament)
        # function being tested
        tournament_id = command_db.add_tournament(tournament)

        # retrieve added tournament from db
        queried_tournament = db_client.session.query(models.Tournament).\
            filter(models.Tournament.id == tournament_id).one()
        # ensure matches expected schema (will raise exception otherwise)
        schemas.Tournament.from_orm(queried_tournament)

        assert queried_tournament.name == tournament.name
        assert queried_tournament.surface == tournament.surface
        assert queried_tournament.draw_size == tournament.draw_size
        assert queried_tournament.level == tournament.level
        assert queried_tournament.start_date == tournament.start_date
