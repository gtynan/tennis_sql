import pytest
from src.db.db import DBClient


@pytest.fixture(scope='session')
def db_client():
    # db instance
    return DBClient(db_name='test_db')


@pytest.fixture(scope='session')
def session(db_client):
    # single session to interact with db
    return db_client._Session()
