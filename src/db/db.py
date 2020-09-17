from typing import Union, List
from datetime import datetime
import numpy as np

from sqlalchemy import event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.exc import FlushError

from ..settings.db import DB_CONFIG

from .models.orm.base import Base as ORMBase
from .models.orm.github import Github as ORMGithub
from .models.pydantic.base import BaseModel
from .models.pydantic.github import Github, GithubCreate


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
        """Any class inheriting ORMBase will have a table generated for them
        """
        ORMBase.metadata.create_all(self.engine)

    def clear_db(self):
        """All rows in all tables will be cleared
        """
        for tbl in reversed(ORMBase.metadata.sorted_tables):
            self.engine.execute(tbl.delete())

    @staticmethod
    def add_own_encoders(conn, cursor, query, *args):
        cursor.connection.encoders[np.int64] = lambda value, encoders: int(value)


class CommandDB:
    '''
    Write side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def ingest_objects(self, objects: List[BaseModel], table: ORMBase, bulk: bool = False) -> None:
        """Handles all ingestion to db

        Args:
            objects (List[BaseModel]): list of objects to be ingested
            table (ORMBase): table to ingest objects into
            bulk (bool, optional): if true will not check for duplicates (should only be true if db empty). Defaults to False.
        """
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

    def _add_object(self, obj: BaseModel, table: ORMBase) -> None:
        self.session.add(table(**obj.dict()))
        self.session.commit()

    def _update_object(self, obj: BaseModel, table: ORMBase) -> None:
        self.session.query(table).\
            filter(table.id == obj.id).update(obj.dict())
        self.session.commit()

    def add_last_ingested_sha(self, sha: str) -> None:
        github = ORMGithub(**GithubCreate(sha=sha).dict())
        self.session.add(github)
        self.session.commit()


class QueryDB:
    '''
    Read side
    '''

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_object_by_id(self, id: Union[int, str], table: ORMBase) -> ORMBase:
        """Given id and table to look in will return object if one

        Args:
            id (Union[int, str]): object id
            table (ORMBase): table object resides in

        Returns:
            ORMBase: Object instance
        """
        return self.session.query(table).\
            filter(table.id == id).one_or_none()

    def get_last_ingested_sha(self) -> str:
        try:
            return self.session.query(ORMGithub).\
                order_by(ORMGithub.date.desc()).first().sha
        except AttributeError:
            return
