from typing import Union, List
from datetime import datetime
import numpy as np

from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from ..settings.db import DB_CONFIG

from .schema.base import BaseTable, Base
from .schema.player import PlayerCreateSchema, PlayerTable
from .schema.tournament import TournamentCreateSchema, TournamentTable
from .schema.game import GameCreateSchema, GameTable
from .schema.performance import PerformanceCreateSchema, WPerformanceTable, LPerformanceTable
from .schema.github import GithubCreateSchema, GithubTable, GithubSchema


class DBClient:

    def __init__(self,
                 db_user: str = DB_CONFIG['db_user'],
                 db_pwd: str = DB_CONFIG['db_pwd'],
                 db_host: str = DB_CONFIG['db_host'],
                 db_port: int = DB_CONFIG['db_port'],
                 db_name: str = DB_CONFIG['db_name']) -> None:
        """Create connection to database

        Args:
            db_user (str, optional): database user name. Defaults to db_config['user'].
            db_pwd (str, optional): database password. Defaults to db_config['password'].
            db_host (str, optional): database host. Defaults to db_config['host'].
            db_port (str, optional): database port. Defaults to db_config['port'].
            db_name (str, optional): database name. Defaults to db_config['database'].
        """

        connection_str = f'mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}'
        self.engine = create_engine(connection_str, echo=True)

        # creates session objects if more needed (used in tests mainly)
        self._Session = sessionmaker(bind=self.engine)
        # session object to communicate with db
        self.session = self._Session()

        # some values are mapped to numpy int so need to convert
        # https://github.com/worldveil/dejavu/issues/142
        event.listen(self.engine, "before_cursor_execute", DBClient.add_own_encoders)

    def generate_schema(self):
        # any class inheriting Base that does not have a table in the db will have one generated for them
        Base.metadata.create_all(self.engine)

    @staticmethod
    def add_own_encoders(conn, cursor, query, *args):
        cursor.connection.encoders[np.int64] = lambda value, encoders: int(value)


class CommandDB:
    '''
    Write side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def _add_instances(self, instances: List[BaseTable]) -> None:
        """Handles all instance additions to the database

        Args:
            instances (List[BaseTable]): instances of db_table that inherits Base
        """
        self.session.add_all(instances)
        self.session.commit()

    def add_players(self, players: List[PlayerCreateSchema]) -> None:
        """Add players to database

        Args:
            players (List[PlayerCreateSchema]): instance of players to add
        """
        players = [PlayerTable(**player.dict()) for player in players]
        self._add_instances(players)

    def add_tournament(self, tournaments: List[TournamentCreateSchema]) -> None:
        """Add tournaments to database

        Args:
            tournaments (List[TournamentCreateSchema]): instances of tournaments to add
        """
        tournaments = [TournamentTable(**tournament.dict()) for tournament in tournaments]
        self._add_instances(tournaments)

    def add_games(self, games: List[GameCreateSchema]) -> None:
        """Add game to database

        Args:
            games (List[GameCreateSchema]): instances of games to add
        """
        games = [GameTable(**game.dict()) for game in games]
        return self._add_instances(games)

    def add_performances(self, performances: List[PerformanceCreateSchema]) -> None:
        """Add performances to database

        Args:
            performances (List[PerformanceCreateSchema]): instances of performances to add
        """
        performances = [WPerformanceTable(**performance.dict()) if performance.won
                        else LPerformanceTable(**performance.dict()) for performance in performances]
        return self._add_instances(performances)

    def add_github_sha(self, sha: str) -> int:
        github = GithubTable(**GithubCreateSchema(sha=sha).dict())
        self.session.add(github)
        self.session.commit()


class QueryDB:
    '''
    Read side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_player_by_id(self, id: int) -> PlayerTable:
        return self.session.query(PlayerTable).\
            filter(PlayerTable.id == id).one_or_none()

    def get_tournament_by_id(self, id: int) -> TournamentTable:
        return self.session.query(TournamentTable).\
            filter(TournamentTable.id == id).one_or_none()

    def get_game_by_id(self, id: int) -> GameTable:
        return self.session.query(GameTable).\
            filter(GameTable.id == id).one_or_none()

    def get_last_github_sha(self) -> str:
        try:
            return self.session.query(GithubTable).\
                order_by(GithubTable.date.desc()).first().sha
        except AttributeError:
            return
