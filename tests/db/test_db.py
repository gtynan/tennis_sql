import pytest
import datetime
import os
import time

from src.db.db import CommandDB, DBClient, QueryDB

from src.db.models.orm.player import Player as ORMPlayer
from src.db.models.pydantic.player import Player, PlayerCreate

from src.db.models.orm.github import Github as ORMGithub


@pytest.fixture(scope='module')
def sample_player() -> PlayerCreate:
    return PlayerCreate(id=200001, first_name='Tom', last_name='Jones', nationality='IRE', dob=datetime.datetime(2000, 1, 1), hand='R')


class TestDBClient:

    def test_init(self, db_client: DBClient):
        '''
        Ensure connected to expected database.
        '''
        assert db_client.engine.url.database == os.getenv('DATABASE') == 'test_db'


class TestCommandDB:

    @pytest.fixture(scope='class')
    def command_db(self, db_client) -> CommandDB:
        return CommandDB(db_client.session)

    def test_ingest_objects(self, db_client, command_db, sample_player):
        sample_player.first_name = 'Jerry'
        command_db.ingest_objects([sample_player], ORMPlayer)

        queried_player = db_client.session.query(ORMPlayer).\
            filter(ORMPlayer.id == sample_player.id).one()
        # will raise error if not of expected schema
        Player.from_orm(queried_player)

        assert queried_player.id == sample_player.id
        assert queried_player.first_name == sample_player.first_name
        assert queried_player.last_name == sample_player.last_name
        assert queried_player.nationality == sample_player.nationality
        assert queried_player.dob == sample_player.dob
        assert queried_player.hand == sample_player.hand

        # ingesting this player again will force function to update instead of add
        sample_player.first_name = 'Tom'
        command_db.ingest_objects([sample_player], ORMPlayer)

        queried_player = db_client.session.query(ORMPlayer).\
            filter(ORMPlayer.id == sample_player.id).one()

        assert queried_player.id == sample_player.id
        assert queried_player.first_name == 'Tom'

    def test_add_last_ingested_sha(self, db_client,  command_db):
        sha = 'TESTSHA101'
        date = datetime.datetime.now()
        command_db.add_last_ingested_sha(sha)

        github_sha = db_client.session.query(ORMGithub).\
            filter(ORMGithub.sha == sha).one()

        assert github_sha.date.day == date.day
        assert github_sha.date.month == date.month
        assert github_sha.date.year == date.year


class TestQueryDB:

    @pytest.fixture(scope='class')
    def query_db(self, db_client) -> QueryDB:
        return QueryDB(db_client.session)

    def test_get_object_by_id(self, query_db, sample_player):
        player = query_db.get_object_by_id(sample_player.id, ORMPlayer)

        assert isinstance(player, ORMPlayer)
        assert player.id == sample_player.id
        assert player.dob == sample_player.dob

    def test_get_last_ingested_sha(self, db_client, query_db):
        # sleep before adding to ensure ate least 1 second between sha dates
        time.sleep(1)

        sha = 'TESTSHA102'
        # adding a second sha to assert it is preferred to one added during TestCommandDB
        db_client.session.add(ORMGithub(sha=sha))
        queried_sha = query_db.get_last_ingested_sha()

        assert queried_sha == sha
