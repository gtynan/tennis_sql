import pytest

from src.db.db import DBClient
from src.db.models.base import BASE
from src.data_scraping import get_raw_players, get_raw_games


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


@pytest.fixture(scope='session')
def sample_players():
    return get_raw_players(n_players=5)


@pytest.fixture(scope='session')
def sample_games():
    return get_raw_games(2020, 2020, n_games=5)
