import pytest

from src.db.db import DBClient
from src.db.tables import Base
from src.data_scraping import get_raw_players, get_raw_games


TEST_DB = 'test_db'


@pytest.fixture(scope='session')
def db_client():
    # db instance
    db_client = DBClient(db_name=TEST_DB)
    yield db_client
    # teardown delete all `Base` created test_db tables
    db_client.session.close()
    for table in reversed(Base.metadata.sorted_tables):
        table.drop(db_client.engine)


@pytest.fixture(scope='session')
def sample_players() -> None:
    return get_raw_players(n_players=5)


@pytest.fixture(scope='session')
def sample_games() -> None:
    return get_raw_games(year_from=2020, year_to=2020, n_games=5)
