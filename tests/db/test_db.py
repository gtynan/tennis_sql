import pytest
import datetime
import numpy as np
import os

from src.db.db import CommandDB, DBClient, QueryDB
from src.constants import WTA_IDENTIFIER

from src.db.schema.player import PlayerTable, PlayerCreateSchema, PlayerSchema
from src.db.schema.tournament import TournamentTable, TournamentCreateSchema, TournamentSchema
from src.db.schema.game import GameTable, GameCreateSchema, GameSchema
from src.db.schema.performance import _PerformanceTable, WPerformanceTable, LPerformanceTable, PerformanceCreateSchema, PerformanceSchema
from src.db.schema.github import GithubTable


@pytest.fixture(scope='module')
def sample_player() -> PlayerCreateSchema:
    return PlayerCreateSchema(id=200001, first_name='Tom', last_name='Jones', nationality='IRE', dob=datetime.datetime(2000, 1, 1), hand='R')


@pytest.fixture(scope='module')
def sample_tournament() -> TournamentCreateSchema:
    return TournamentCreateSchema(id='2020-1049', name='Aus Open', surface='Hard', draw_size=32, level='G', start_date=datetime.datetime(2000, 1, 1))


@pytest.fixture(scope='module')
def sample_game(sample_tournament) -> GameCreateSchema:
    return GameCreateSchema(id=f'{sample_tournament.id}_1', score='6-0 6-0', round='R32', circuit=WTA_IDENTIFIER, tournament_id=sample_tournament.id)


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

    def test_add_players(self, db_client, command_db, sample_player):
        command_db.add_players([sample_player])

        queried_player = db_client.session.query(PlayerTable).\
            filter(PlayerTable.id == sample_player.id).one()
        # ensure matches expected schema (will raise exception otherwise)
        PlayerSchema.from_orm(queried_player)

        assert queried_player.first_name == sample_player.first_name
        assert queried_player.last_name == sample_player.last_name
        assert queried_player.nationality == sample_player.nationality
        assert queried_player.dob == sample_player.dob
        assert queried_player.hand == sample_player.hand
        assert queried_player.name == sample_player.first_name + " " + sample_player.last_name

    def test_add_tournaments(self, db_client, command_db, sample_tournament):
        # convert to pydantic object to validate insert schema
        command_db.add_tournaments([sample_tournament])

        queried_tournament = db_client.session.query(TournamentTable).\
            filter(TournamentTable.id == sample_tournament.id).one()
        # ensure matches expected schema (will raise exception otherwise)
        TournamentSchema.from_orm(queried_tournament)

        assert queried_tournament.name == sample_tournament.name
        assert queried_tournament.surface == sample_tournament.surface
        assert queried_tournament.draw_size == sample_tournament.draw_size
        assert queried_tournament.level == sample_tournament.level
        assert queried_tournament.start_date == sample_tournament.start_date

    def test_add_games(self, db_client, command_db, sample_game):
        # convert to pydantic object to validate insert schema
        command_db.add_games([sample_game])

        queried_game = db_client.session.query(GameTable).\
            filter(GameTable.id == sample_game.id).one()
        # ensure matches expected schema (will raise exception otherwise)
        GameSchema.from_orm(queried_game)

        assert queried_game.tournament_id == sample_game.tournament_id
        assert queried_game.score == sample_game.score
        assert queried_game.round == sample_game.round
        assert queried_game.circuit == sample_game.circuit

    def test_add_performances(self, db_client, command_db, sample_player, sample_game):
        w_performance = PerformanceCreateSchema(won=True, player_id=sample_player.id, game_id=sample_game.id)
        l_performance = PerformanceCreateSchema(won=False, player_id=sample_player.id, game_id=sample_game.id)

        command_db.add_performances([w_performance, l_performance])

        queried_performances = db_client.session.query(_PerformanceTable).\
            filter(_PerformanceTable.player_id == sample_player.id).all()

        # ensure matches expected schema (will raise exception otherwise)
        [PerformanceSchema.from_orm(queried_performance) for queried_performance in queried_performances]

        assert isinstance(queried_performances[0], WPerformanceTable)
        assert isinstance(queried_performances[1], LPerformanceTable)
        assert queried_performances[0].game_id == queried_performances[1].game_id == sample_game.id
        assert queried_performances[0].player.id == queried_performances[1].player.id == sample_player.id
        assert queried_performances[0].won
        assert ~queried_performances[1].won

    def test_add_github_sha(self, db_client,  command_db):
        sha = 'TESTSHA101'
        date = datetime.datetime.now()
        command_db.add_github_sha(sha)

        github_sha = db_client.session.query(GithubTable).\
            filter(GithubTable.sha == sha).one()

        assert github_sha.date.day == date.day
        assert github_sha.date.month == date.month
        assert github_sha.date.year == date.year


class TestQueryDB:

    @pytest.fixture(scope='class')
    def query_db(self, db_client) -> QueryDB:
        return QueryDB(db_client.session)

    def test_get_player_by_id(self, query_db, sample_player):
        player = query_db.get_player_by_id(sample_player.id)

        assert isinstance(player, PlayerTable)
        assert player.id == sample_player.id
        assert player.name == sample_player.first_name + " " + sample_player.last_name
        assert player.dob == sample_player.dob

    def test_get_tournament_by_id(self, query_db, sample_tournament):
        tournament = query_db.get_tournament_by_id(sample_tournament.id)

        assert isinstance(tournament, TournamentTable)
        assert tournament.id == sample_tournament.id
        assert tournament.name == sample_tournament.name

    def test_get_game_by_id(self, query_db, sample_game, sample_tournament):
        game = query_db.get_game_by_id(sample_game.id)

        assert isinstance(game, GameTable)
        assert game.id == sample_game.id
        assert game.tournament.name == sample_tournament.name

    def test_get_last_github_sha(self, db_client, query_db):
        sha = 'TESTSHA102'

        # adding a second sha to assert it is not returned
        db_client.session.add(GithubTable(sha=sha))

        queried_sha = query_db.get_last_github_sha()

        assert queried_sha != sha
        assert isinstance(queried_sha, str)
