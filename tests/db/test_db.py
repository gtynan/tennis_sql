import pytest
import datetime
import numpy as np

from src.db_models.player import Player
from src.db.db import CommandDB
from ..conftest import TEST_DB


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
