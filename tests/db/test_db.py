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
def sample_player() -> PlayerTable:
    return PlayerTable(first_name='Tom', last_name='Jones', nationality='IRE', dob=datetime.datetime(2000, 1, 1), hand='R')


@pytest.fixture(scope='module')
def sample_tournament() -> TournamentTable:
    return TournamentTable(name='Aus Open', surface='Hard', draw_size=32, level='G', start_date=datetime.datetime(2000, 1, 1))


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
        # convert to pydantic object to validate insert schema
        player = PlayerCreateSchema.from_orm(sample_player)
        command_db.add_players([player])

        queried_player = db_client.session.query(PlayerTable).\
            filter(PlayerTable.name == sample_player.name).one()
        # ensure matches expected schema (will raise exception otherwise)
        PlayerSchema.from_orm(queried_player)

        assert queried_player.first_name == player.first_name
        assert queried_player.last_name == player.last_name
        assert queried_player.nationality == player.nationality
        assert queried_player.dob == player.dob
        assert queried_player.hand == player.hand
        assert queried_player.name == player.first_name + " " + player.last_name

    def test_add_tournaments(self, db_client, command_db, sample_tournament):
        # convert to pydantic object to validate insert schema
        tournament = TournamentCreateSchema.from_orm(sample_tournament)
        command_db.add_tournaments([tournament])

        queried_tournament = db_client.session.query(TournamentTable).\
            filter(TournamentTable.name == sample_tournament.name).one()
        # ensure matches expected schema (will raise exception otherwise)
        TournamentSchema.from_orm(queried_tournament)

        assert queried_tournament.name == tournament.name
        assert queried_tournament.surface == tournament.surface
        assert queried_tournament.draw_size == tournament.draw_size
        assert queried_tournament.level == tournament.level
        assert queried_tournament.start_date == tournament.start_date

    def test_add_games(self, db_client, command_db, sample_tournament):
        tournament_id = db_client.session.query(TournamentTable).\
            filter(TournamentTable.name == sample_tournament.name).one().id

        game = GameCreateSchema(score='6-0 6-0', round='R32', circuit=WTA_IDENTIFIER, tournament_id=tournament_id)
        command_db.add_games([game])

        queried_game = db_client.session.query(GameTable).\
            filter(GameTable.score == game.score).one()
        # ensure matches expected schema (will raise exception otherwise)
        GameSchema.from_orm(queried_game)

        assert queried_game.tournament_id == tournament_id
        assert queried_game.score == game.score
        assert queried_game.round == game.round
        assert queried_game.circuit == game.circuit

    def test_add_performances(self, db_client, command_db, sample_tournament, sample_player):
        # id's needed to create performance object
        tournament_id = db_client.session.query(TournamentTable).\
            filter(TournamentTable.name == sample_tournament.name).one().id
        game_id = db_client.session.query(GameTable).\
            filter(GameTable.tournament_id == tournament_id).one().id
        player_id = db_client.session.query(PlayerTable).\
            filter(PlayerTable.name == sample_player.name).\
            filter(PlayerTable.dob == sample_player.dob).one().id

        w_performance = PerformanceCreateSchema(won=True, player_id=player_id, game_id=game_id)
        l_performance = PerformanceCreateSchema(won=False, player_id=player_id, game_id=game_id)

        command_db.add_performances([w_performance, l_performance])

        queried_performances = db_client.session.query(_PerformanceTable).\
            filter(_PerformanceTable.player_id == player_id).all()

        # ensure matches expected schema (will raise exception otherwise)
        [PerformanceSchema.from_orm(queried_performance) for queried_performance in queried_performances]

        assert isinstance(queried_performances[0], WPerformanceTable)
        assert isinstance(queried_performances[1], LPerformanceTable)
        assert queried_performances[0].game_id == queried_performances[1].game_id == game_id
        assert queried_performances[0].player.id == queried_performances[1].player.id == player_id
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
        player = query_db.get_player_by_id(1)

        assert isinstance(player, PlayerTable)
        assert player.id == 1
        assert player.name == sample_player.name
        assert player.dob == sample_player.dob

    def test_get_tournament_by_id(self, query_db, sample_tournament):
        tournament = query_db.get_tournament_by_id(1)

        assert isinstance(tournament, TournamentTable)
        assert tournament.id == 1
        assert tournament.name == sample_tournament.name

    def test_get_game_by_id(self, query_db, sample_tournament, sample_player):
        game = query_db.get_game_by_id(1)

        assert isinstance(game, GameTable)
        assert game.id == 1
        assert game.tournament.name == sample_tournament.name

    def test_get_last_github_sha(self, db_client,  query_db):
        sha = 'TESTSHA102'

        # adding a second sha to assert it is not returned
        db_client.session.add(GithubTable(sha=sha))

        queried_sha = query_db.get_last_github_sha()

        assert queried_sha != sha
        assert isinstance(queried_sha, str)
