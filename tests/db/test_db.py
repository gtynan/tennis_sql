import pytest

def test_init(db):
    assert db.engine.url.database == 'test_db' 
