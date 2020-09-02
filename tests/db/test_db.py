import pytest
import datetime
import numpy as np

from ..conftest import TEST_DB
from src.db.db import CommandDB, QueryDB
from src.db.models.player import Player
from src.db.models.tournament import Tournament


class TestDBClient:

    def test_init(self, db_client):
        '''
        Ensure connected to expected database.
        '''
        assert db_client.engine.url.database == TEST_DB


class TestCommandDB:

    @pytest.fixture(scope='module')
    def command_db(self, db_client) -> CommandDB:
        return CommandDB(db_client)

    def test_add_player(self, db_client, command_db):
        fname, lname, nation, dob, hand = 'Tom', 'Jones', 'IRE', datetime.date(2000, 1, 1), 'R'
        player = Player(first_name=fname, last_name=lname, nationality=nation, dob=dob, hand=hand)

        command_db.add_player(player)

        # will raise exception if there is anything other than 1 instance present
        db_client.session.query(Player).\
            filter(Player.first_name == fname).\
            filter(Player.last_name == lname).\
            filter(Player.nationality == nation).\
            filter(Player.dob == dob).\
            filter(Player.hand == hand).one()

    def test_add_tournament(self, db_client, command_db):
        name, surface, draw_size, level, start_date = 'Aus Open', 'Hard', 32, 'G', datetime.date(2000, 1, 1)
        tournament = Tournament(name=name, surface=surface, draw_size=draw_size, level=level, start_date=start_date)

        command_db.add_tournament(tournament)

        # will raise exception if there is anything other than 1 instance present
        db_client.session.query(Tournament).\
            filter(Tournament.name == name).\
            filter(Tournament.surface == surface).\
            filter(Tournament.draw_size == draw_size).\
            filter(Tournament.level == level).\
            filter(Tournament.start_date == start_date).one()


class TestQueryDB:

    @pytest.fixture(scope='module')
    def query_db(self, db_client) -> QueryDB:
        return QueryDB(db_client)

    def test_get_player(self, query_db):
        fname, lname, dob = "Tom", "Jones", datetime.date(2000, 1, 1)
        player = query_db.get_player(fname, lname, dob)

        assert player.first_name == fname
        assert player.last_name == lname
        assert player.dob == dob
        assert query_db.get_player("Test", "Player", datetime.date.today()) is None

    def test_get_tournament(self, query_db):
        name, start_date = 'Aus Open', datetime.date(2000, 1, 1)
        tournament = query_db.get_tournament(name, start_date)

        assert tournament.name == name
        assert tournament.start_date == start_date
        assert query_db.get_tournament("Test", datetime.date.today()) is None
