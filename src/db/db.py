from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

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
        '''
        Writes players to database
        '''
        self.db_client.session.add(player)
        self.db_client.session.commit()
