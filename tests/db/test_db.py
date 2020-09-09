import pytest
import datetime
import numpy as np

from ..conftest import TEST_DB
from src.db.db import CommandDB, DBClient, QueryDB
from src.constants import WTA_IDENTIFIER

from src.db.schema.player import PlayerTable, PlayerCreateSchema, PlayerSchema
from src.db.schema.tournament import TournamentTable, TournamentCreateSchema, TournamentSchema
from src.db.schema.game import GameTable, GameCreateSchema, GameSchema
from src.db.schema.performance import _PerformanceTable, WPerformanceTable, LPerformanceTable, PerformanceCreateSchema, PerformanceSchema


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
        assert db_client.engine.url.database == TEST_DB


class TestCommandDB:

    @pytest.fixture(scope='class')
    def command_db(self, db_client) -> CommandDB:
        return CommandDB(db_client.session)

    def test_add_player(self, db_client, command_db, sample_player):
        # convert to pydantic object to validate insert schema
        player = PlayerCreateSchema.from_orm(sample_player)
        player_id = command_db.add_player(player)

        queried_player = db_client.session.query(PlayerTable).\
            filter(PlayerTable.id == player_id).one()
        # ensure matches expected schema (will raise exception otherwise)
        PlayerSchema.from_orm(queried_player)

        assert queried_player.first_name == player.first_name
        assert queried_player.last_name == player.last_name
        assert queried_player.nationality == player.nationality
        assert queried_player.dob == player.dob
        assert queried_player.hand == player.hand
        assert queried_player.name == player.first_name + " " + player.last_name

    def test_add_tournament(self, db_client, command_db, sample_tournament):
        # convert to pydantic object to validate insert schema
        tournament = TournamentCreateSchema.from_orm(sample_tournament)
        tournament_id = command_db.add_tournament(tournament)

        queried_tournament = db_client.session.query(TournamentTable).\
            filter(TournamentTable.id == tournament_id).one()
        # ensure matches expected schema (will raise exception otherwise)
        TournamentSchema.from_orm(queried_tournament)

        assert queried_tournament.name == tournament.name
        assert queried_tournament.surface == tournament.surface
        assert queried_tournament.draw_size == tournament.draw_size
        assert queried_tournament.level == tournament.level
        assert queried_tournament.start_date == tournament.start_date

    def test_add_game(self, db_client, command_db, sample_tournament):
        tournament_id = db_client.session.query(TournamentTable).\
            filter(TournamentTable.name == sample_tournament.name).one().id

        game = GameCreateSchema(score='6-0 6-0', round='R32', circuit=WTA_IDENTIFIER, tournament_id=tournament_id)
        game_id = command_db.add_game(game)

        queried_game = db_client.session.query(GameTable).\
            filter(GameTable.id == game_id).one()
        # ensure matches expected schema (will raise exception otherwise)
        GameSchema.from_orm(queried_game)

        assert queried_game.id == game_id
        assert queried_game.tournament_id == tournament_id
        assert queried_game.score == game.score
        assert queried_game.round == game.round
        assert queried_game.circuit == game.circuit

    def test_add_performance(self, db_client, command_db, sample_tournament, sample_player):
        # id's needed to create performance object
        tournament_id = db_client.session.query(TournamentTable).\
            filter(TournamentTable.name == sample_tournament.name).one().id
        game_id = db_client.session.query(GameTable).\
            filter(GameTable.tournament_id == tournament_id).one().id
        player_id = db_client.session.query(PlayerTable).\
            filter(PlayerTable.name == sample_player.name).\
            filter(PlayerTable.dob == sample_player.dob).one().id

        performance_id = command_db.add_performance(
            performance=PerformanceCreateSchema(won=True, player_id=player_id, game_id=game_id))

        queried_performance = db_client.session.query(_PerformanceTable).\
            filter(_PerformanceTable.id == performance_id).one()
        # ensure matches expected schema (will raise exception otherwise)
        PerformanceSchema.from_orm(queried_performance)

        assert isinstance(queried_performance, WPerformanceTable)
        assert queried_performance.game_id == game_id
        assert queried_performance.player.id == player_id
        assert queried_performance.won

        # add performance, won=True should update games w_performance thus ensure games accessible via game
        queried_game = db_client.session.query(GameTable).\
            filter(GameTable.id == game_id).one()
        assert queried_game.w_performance.id == queried_performance.id

        # test LPerformance, won=False should create LPerformance  instance
        performance_id = command_db.add_performance(
            performance=PerformanceCreateSchema(won=False, player_id=player_id, game_id=game_id))

        # query LPerformance table to ensure mapped correctly
        queried_performance = db_client.session.query(_PerformanceTable).\
            filter(_PerformanceTable.id == performance_id).one()
        # ensure meets expected schema
        PerformanceSchema.from_orm(queried_performance)

        assert isinstance(queried_performance, LPerformanceTable)
        assert queried_performance.game_id == game_id
        assert queried_performance.player.id == player_id
        assert ~queried_performance.won


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
