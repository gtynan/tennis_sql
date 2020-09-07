import pytest
import datetime
import numpy as np

from ..conftest import TEST_DB
from src.db.db import CommandDB, QueryDB, DBClient
from src.db.models import Player, Tournament, Performance, WTA, ITF

from src.db.schemas import PlayerCreate


@pytest.fixture(scope='module')
def sample_player() -> Player:
    return Player(first_name='Tom', last_name='Jones', nationality='IRE', dob=datetime.datetime(2000, 1, 1), hand='R')


@pytest.fixture(scope='module')
def sample_tournament() -> Tournament:
    return Tournament(name='Aus Open', surface='Hard', draw_size=32, level='G', start_date=datetime.date(2000, 1, 1))


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
        player = PlayerCreate(first_name=sample_player.first_name, last_name=sample_player.last_name,
                              nationality=sample_player.nationality, dob=sample_player.dob, hand=sample_player.hand)

        command_db.add_player(player)

        # will raise exception if there is anything other than 1 instance present
        db_client.session.query(Player).\
            filter(Player.first_name == sample_player.first_name).\
            filter(Player.last_name == sample_player.last_name).\
            filter(Player.nationality == sample_player.nationality).\
            filter(Player.dob == sample_player.dob).\
            filter(Player.hand == sample_player.hand).one()

    def test_add_tournament(self, db_client, command_db, sample_tournament):
        command_db.add_tournament(sample_tournament)

        # will raise exception if there is anything other than 1 instance present
        db_client.session.query(Tournament).\
            filter(Tournament.name == sample_tournament.name).\
            filter(Tournament.surface == sample_tournament.surface).\
            filter(Tournament.draw_size == sample_tournament.draw_size).\
            filter(Tournament.level == sample_tournament.level).\
            filter(Tournament.start_date == sample_tournament.start_date).one()

    def test_add_game(self, db_client, command_db, sample_player, sample_tournament):
        # changing names to avoid adding multiple instances of same player
        w_performance = Performance(player=sample_player)
        w_performance.player.first_name = "Ben"
        l_performance = Performance(player=sample_player)
        l_performance.player.first_name = "Fran"

        game = WTA(tournament=sample_tournament, w_performance=w_performance, l_performance=l_performance)

        command_db.add_game(game)

        db_client.session.query(WTA).\
            filter(WTA.tournament == sample_tournament).\
            filter(WTA.w_performance == w_performance).\
            filter(WTA.l_performance == l_performance).one()


class TestQueryDB:

    @pytest.fixture(scope='class')
    def query_db(self, db_client) -> QueryDB:
        return QueryDB(db_client.session)

    def test_get_player(self, query_db, sample_player):
        player = query_db.get_player(sample_player.name, sample_player.dob)

        assert player.name == sample_player.name
        assert query_db.get_player("Test Player", datetime.date.today()) is None

    def test_get_tournament(self, query_db, sample_tournament):
        tournament = query_db.get_tournament(sample_tournament.name, sample_tournament.start_date)

        assert tournament.name == sample_tournament.name
        assert query_db.get_tournament("Test", datetime.date.today()) is None

    def test_get_game(self, query_db, sample_tournament, sample_player):
        ben, fran = sample_player, sample_player
        ben.first_name, fran.first_name = "Ben", "Fran"

        game = query_db.get_game(sample_tournament, ben, fran)

        assert game.tournament == sample_tournament
        assert game.w_performance.player.name == ben.name
        assert game.l_performance.player.name == fran.name
        assert game.circuit == 'wta'
