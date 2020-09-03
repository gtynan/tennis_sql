from typing import Union
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from ._secrets import db_config
from .models.base import BASE
from .models.player import Player
from .models.tournament import Tournament
from .models.performance import Performance
from .models.game import _Game


class DBClient:

    def __init__(self,
                 db_user: str = db_config['user'],
                 db_pwd: str = db_config['password'],
                 db_host: str = db_config['host'],
                 db_port: str = db_config['port'],
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
        BASE.metadata.create_all(self.engine)

        # creates session objects if more needed (used in tests mainly)
        self._Session = sessionmaker(bind=self.engine)
        # session object to communicate with db
        self.session = self._Session()


class CommandDB:
    '''
    Write side
    '''

    def __init__(self, db_client: DBClient) -> None:
        self.db_client = db_client

    def _add_instance(self, instance: BASE):
        """Handles all single instance additions to the database

        Args:
            instance (BASE): instance of db_table that inherits BASE
        """
        self.db_client.session.add(instance)
        self.db_client.session.commit()

    def add_player(self, player: Player) -> None:
        """Add player to database

        Args:
            player (Player): instance of player to add
        """
        self._add_instance(player)

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

    def __init__(self, db_client: DBClient) -> None:
        self.db_client = db_client

    def get_player(self, first_name: str, last_name: str, dob: datetime) -> Player:
        """Get player from database

        Args:
            first_name (str): player's first name
            last_name (str): player's last name
            dob (datetime): player's date of birth

        Returns:
            Player: instance of queried player
        """
        try:
            return self.db_client.session.query(Player).\
                filter(Player.first_name == first_name).\
                filter(Player.last_name == last_name).\
                filter(Player.dob == dob).one_or_none()
        except MultipleResultsFound:
            raise Exception("Multiple instances of same player found.")

    def get_tournament(self, name: str, start_date: datetime) -> Tournament:
        """Get tournament from database

        Args:
            name (str): tournament name
            start_date (datetime): tournament start date

        Returns:
            Tournament: instance of queried tournamnet
        """
        try:
            return self.db_client.session.query(Tournament).\
                filter(Tournament.name == name).\
                filter(Tournament.start_date == start_date).one_or_none()
        except MultipleResultsFound:
            raise Exception("Multiple instances of same tournament found.")

    def get_game(self, tournament: Tournament, w_player: Player, l_player: Player) -> _Game:
        try:
            return self.db_client.session.query(_Game).\
                filter(_Game.tournament == tournament).\
                filter(_Game.w_performance.has(Performance.player == w_player)).\
                filter(_Game.l_performance.has(Performance.player == l_player)).one_or_none()
        except MultipleResultsFound:
            raise Exception("Multiple instances of same game found.")
