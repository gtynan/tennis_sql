import pytest
from fastapi.testclient import TestClient

from src.main import app as app


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


def test_read_player_by_id(client):
    response = client.get('/player/1')
    assert response.status_code == 404


def test_read_tournament_by_id(client):
    response = client.get('/tournament/1')
    assert response.status_code == 404


def test_read_game_by_id(client):
    response = client.get('/game/1')
    assert response.status_code == 404
