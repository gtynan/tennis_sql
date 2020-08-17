import pytest


def test_init(db_client):
    # TODO test tables created via base
    assert db_client.engine.url.database == 'test_db'
