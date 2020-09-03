import pytest

from src.db.db import DBClient
from src.db.models.base import BASE


TEST_DB = 'test_db'


@pytest.fixture(scope='session')
def db_client():
    # db instance
    db_client = DBClient(db_name=TEST_DB)
    yield db_client
    # teardown delete all `Base` created test_db tables
    db_client.session.close()
    for table in reversed(BASE.metadata.sorted_tables):
        table.drop(db_client.engine)
