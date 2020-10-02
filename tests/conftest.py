import pytest
import pandas as pd

from src.db.db import DBClient
from src.db.models.orm.base import Base
from src.constants import PLAYER_URL, GAME_SOURCES, WTA_IDENTIFIER


@pytest.fixture(scope='session')
def db_client():
    # db instance
    db_client = DBClient()
    # creates database schema
    db_client.generate_schema()
    yield db_client
    # teardown delete all `Base` created test_db tables
    db_client.session.close()
    with db_client.engine.connect() as conn:
        Base.metadata.drop_all(conn, checkfirst=False)


@pytest.fixture(scope='session')
def sample_players():
    """Gets 5 sample WTA players"""
    return pd.read_csv(PLAYER_URL, nrows=5)


@pytest.fixture(scope='session')
def sample_games():
    """Gets 5 sample WTA players"""
    games_2020_url = GAME_SOURCES[WTA_IDENTIFIER].format(2020)
    return pd.read_csv(games_2020_url, nrows=5)
