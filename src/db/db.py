from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from ._secrets import db_config
from ..db_models.base import BASE
from ..db_models.player import Player


class DBClient:

    def __init__(self,
                 db_user: str = db_config['user'],
                 db_pwd: str = db_config['password'],
                 db_host: str = db_config['host'],
                 db_port: str = db_config['port'],
                 db_name: str = db_config['database']) -> None:

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

    def add_player(self, player: Player) -> None:
        """Add player to database

        Args:
            player (Player): instance of player to add
        """
        self.db_client.session.add(player)
        self.db_client.session.commit()


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
