from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from ._secrets import db_config

Base = declarative_base()

class Database:

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
