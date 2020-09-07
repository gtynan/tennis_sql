from typing import Union
from datetime import datetime
import numpy as np

from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from ._secrets import db_config
from .models import Base, Player, Tournament, Performance, _Game

from .schemas import PlayerCreate


class DBClient:

    def __init__(self,
                 db_user: str = db_config['user'],
                 db_pwd: str = db_config['password'],
                 db_host: str = db_config['host'],
                 db_port: int = db_config['port'],
                 db_name: str = db_config['database']) -> None:
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

        # any class inheriting Base that does not have a table in the db will have one generated for them
        Base.metadata.create_all(self.engine)

        # creates session objects if more needed (used in tests mainly)
        self._Session = sessionmaker(bind=self.engine)
        # session object to communicate with db
        self.session = self._Session()

        # some values are mapped to numpy int so need to convert
        # https://github.com/worldveil/dejavu/issues/142
        event.listen(self.engine, "before_cursor_execute", DBClient.add_own_encoders)

    @staticmethod
    def add_own_encoders(conn, cursor, query, *args):
        cursor.connection.encoders[np.int64] = lambda value, encoders: int(value)


class CommandDB:
    '''
    Write side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def _add_instance(self, instance: Base):
        """Handles all single instance additions to the database

        Args:
            instance (BASE): instance of db_table that inherits BASE
        """
        self.session.add(instance)
        self.session.commit()

    def add_player(self, player: PlayerCreate) -> None:
        """Add player to database

        Args:
            player (Player): instance of player to add
        """
        self._add_instance(Player(**player.dict()))

    def add_tournament(self, tournament: Tournament) -> None:
        """Add tournament to database

        Args:
            tournament (Tournament): instance of tournament to add
        """
        self._add_instance(tournament)

    def add_game(self, game: _Game) -> None:
        """Add game to database

        Args:
            game (_Game): instance of game
        """
        self._add_instance(game)


class QueryDB:
    '''
    Read side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_player(self, name: str, dob: datetime) -> Player:
        """Get player from database

        Args:
            first_name (str): player's first name
            last_name (str): player's last name
            dob (datetime): player's date of birth

        Raises:
            Exception: If multiple results found

        Returns:
            Player: instance of queried player
        """
        try:
            return self.session.query(Player).\
                filter(Player.name == name).\
                filter(Player.dob == dob).one_or_none()
        except MultipleResultsFound:
            raise Exception("Multiple instances of same player found.")

    def get_tournament(self, name: str, start_date: datetime) -> Tournament:
        """Get tournament from database

        Args:
            name (str): tournament name
            start_date (datetime): tournament start date

        Raises:
            Exception: If multiple results found

        Returns:
            Tournament: instance of queried tournamnet
        """
        try:
            return self.session.query(Tournament).\
                filter(Tournament.name == name).\
                filter(Tournament.start_date == start_date).one_or_none()
        except MultipleResultsFound:
            raise Exception("Multiple instances of same tournament found.")

    def get_game(self, tournament: Tournament, w_player: Player, l_player: Player) -> _Game:
        """Get game from database

        Args:
            tournament (Tournament): tournament object
            w_player (Player): winning player object
            l_player (Player): loseing player object

        Raises:
            Exception: If multiple results found

        Returns:
            _Game: instance of queried game
        """
        try:
            return self.session.query(_Game).\
                filter(_Game.tournament == tournament).\
                filter(_Game.w_performance.has(Performance.player == w_player)).\
                filter(_Game.l_performance.has(Performance.player == l_player)).one_or_none()
        except MultipleResultsFound:
            raise Exception("Multiple instances of same game found.")
