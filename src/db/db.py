from typing import List
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound

from ._secrets import db_config
from .tables import Base, Player

'''
Seperating read and write responsibilies
'''


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
        Base.metadata.create_all(self.engine)

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
        # some writes require read to ensure no duplicates
        self.query_db = QueryDB(db_client)

    def create_players(self, players: List[Player], check_duplicates: bool = True) -> None:
        '''
        Writes players to database

        args:
            check_duplicates: if true will not add players already in db
        '''
        if check_duplicates:
            # for each player check if exists, if not add
            for player in players:
                try:
                    self.query_db.read_player(
                        player.fname, player.lname, player.dob)
                except NoResultFound:
                    self.db_client.session.add(player)
        else:
            self.db_client.session.add_all(players)
        self.db_client.session.commit()


class QueryDB:
    '''
    Read side
    '''

    def __init__(self, db_client: DBClient):
        self.db_client = db_client

    def read_player(self, fname: str, lname: str, dob: datetime) -> Player:
        '''
        Gets player from db, raises error if none or more than one instance

        args:
            fname: first name
            lname: last name
            dob: date of birth
        '''
        return self.db_client.session.query(Player).\
            filter(Player.fname == fname).\
            filter(Player.lname == lname).\
            filter(Player.dob == dob).one()
