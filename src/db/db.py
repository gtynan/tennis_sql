from typing import Union
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

    def _add_instance(self, instance: BaseTable) -> int:
        """Handles all single instance additions to the database

        Args:
            instance (BaseTable): instance of db_table that inherits Base

        Returns:
            int: instance id in table
        """
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)
        return instance.id

    def add_player(self, player: PlayerCreateSchema) -> int:
        """Add player to database

        Args:
            player (PlayerCreateSchema): instance of player to add

        Returns:
            int: player id of added player
        """
        player = PlayerTable(**player.dict())
        return self._add_instance(player)

    def add_tournament(self, tournament: TournamentCreateSchema) -> int:
        """Add tournament to database

        Args:
            tournament (TournamentCreateSchema): instance of tournament to add

        Returns:
            int: tournament id of added tournament
        """
        tournament = TournamentTable(**tournament.dict())
        return self._add_instance(tournament)

    def add_game(self, game: GameCreateSchema) -> int:
        """Add game to database

        Args:
            game (GameCreateSchema): instance of game to add
            tournament_id (int): id of tournament game played in

        Returns:
            int: game id of added game
        """
        game = GameTable(**game.dict())
        return self._add_instance(game)

    def add_performance(self, performance: PerformanceCreateSchema) -> int:
        """Add performance to database

        Args:
            performance (PerformanceCreateSchema): instance of performance to add
            player_id (int): id of player who the performance relates to 
            game_id (int): id of game performance relates ot 

        Returns:
            int: performance id of added performance
        """
        if performance.won:
            return self._add_instance(WPerformanceTable(**performance.dict()))
        else:
            return self._add_instance(LPerformanceTable(**performance.dict()))


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
