import pytest
from src.db.db import Database

# db instance
@pytest.fixture(scope='session')
def db():
    return Database(db_name='test_db')

# single session to interact with db
@pytest.fixture(scope='session')
def session(db):
    return db._Session()
