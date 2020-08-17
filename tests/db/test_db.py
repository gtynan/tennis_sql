import pytest
from datetime import datetime
import numpy as np

from sqlalchemy import inspect
from sqlalchemy.orm.exc import MultipleResultsFound

from src.constants import player_csv_map
from ..conftest import TEST_DB
from src.db.db import CommandDB, QueryDB
from src.db.tables import Player
from src.data_scraping import get_raw_players
from src.data_cleaning import raw_player_to_object

# tables to check for in TestDBClient test_schema
TABLE_CLASSES = [Player()]


@pytest.fixture(scope='module')
def query_db(db_client) -> QueryDB:
    # shared by both TestCommand and TestQuery
    return QueryDB(db_client)


class TestDBClient:

    def test_init(self, db_client):
        '''
        Ensure connected to expected database.
        '''
        assert db_client.engine.url.database == TEST_DB

    def test_schema(self, db_client):
        '''
        Ensure all tables in the src/db/tables module with Base parent are in the database
        '''
        db_inspector = inspect(db_client.engine)
        db_tables = db_inspector.get_table_names()

        # ensure ecpetced tables present
        assert np.isin(
            [table.__tablename__ for table in TABLE_CLASSES],
            db_tables).all()

        # ensure table matches expected schema
        for table_class in TABLE_CLASSES:
            for db_column in db_inspector.get_columns(table_class.__tablename__):
                assert hasattr(table_class, db_column['name'])


class TestCommandDB:

    @pytest.fixture(scope='class')
    def command_db(self, db_client) -> CommandDB:
        return CommandDB(db_client)

    @pytest.mark.slow
    def test_create_players(self, command_db, query_db, sample_players):
        '''
        Gets players adds them twice and ensures no duplictaes were added.
        '''
        raw_players = sample_players
        clean_players = raw_players.apply(
            lambda x: raw_player_to_object(x), axis=1).to_list()

        # no players will have been added due to conftest teardown thus no need to check
        command_db.create_players(clean_players, check_duplicates=False)

        raw_players = get_raw_players(n_players=len(raw_players) + 1)
        clean_players = raw_players.apply(
            lambda x: raw_player_to_object(x), axis=1).to_list()

        # check duplicates should ensure nothing added except last row (+1)
        command_db.create_players(clean_players, check_duplicates=True)

        # check all players added, raises error if not
        for player in clean_players:
            query_db.read_player(player.fname, player.lname, player.dob)


class TestQueryDB:

    def test_read_player(self, query_db, sample_players):
        player = sample_players.iloc[0]

        read_player = query_db.read_player(
            fname=player[player_csv_map['fname']],
            lname=player[player_csv_map['lname']],
            dob=datetime.strptime(str(player[player_csv_map['dob']]), '%Y%m%d')
        )
        # check the two variables not given to read match expectecd
        assert player[player_csv_map['nationality']] == read_player.nationality
        assert player[player_csv_map['hand']] == read_player.hand
