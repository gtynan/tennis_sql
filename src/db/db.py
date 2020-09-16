from typing import Union, List
from datetime import datetime
import numpy as np

from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import FlushError

from ..settings.db import DB_CONFIG

from .schema.base import BaseTable, Base, BaseModel
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

    def ingest_objects(self, objects: List[BaseModel], table: BaseTable, bulk: bool = False) -> None:
        if bulk:
            objects = [table(**obj.dict()) for obj in objects]
            self.session.add_all(objects)
            self.session.commit()
        else:
            for obj in objects:
                try:
                    self._add_object(obj, table)
                except FlushError:
                    self.session.rollback()
                    self._update_object(obj, table)

    def _add_object(self, obj: BaseModel, table: BaseTable) -> None:
        self.session.add(table(**obj.dict()))
        self.session.commit()

    def _update_object(self, obj: BaseModel, table: BaseTable) -> None:
        self.session.query(table).\
            filter(table.id == obj.id).update(obj.dict())
        self.session.commit()

    def add_last_ingested_sha(self, sha: str) -> int:
        github = GithubTable(**GithubCreateSchema(sha=sha).dict())
        self.session.add(github)
        self.session.commit()


class QueryDB:
    '''
    Read side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_object_by_id(self, id: Union[int, str], table: BaseTable) -> BaseTable:
        return self.session.query(table).\
            filter(table.id == id).one_or_none()

    def get_last_ingested_sha(self) -> str:
        try:
            return self.session.query(GithubTable).\
                order_by(GithubTable.date.desc()).first().sha
        except AttributeError:
            return
