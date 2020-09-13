import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from src.main import app as app
from src.db.schema.player import PlayerTable, PlayerSchema
from src.db.schema.tournament import TournamentTable, TournamentSchema
from src.db.schema.game import GameTable, GameSchema
from src.constants import WTA_IDENTIFIER

'''
DB begins empty, so tests first assert no API response then adds data and asserts response 
'''


@pytest.fixture(scope='module')
def client():
    return TestClient(app)


def test_read_player_by_id(client, db_client):
    response = client.get('/player/1')
    assert response.status_code == 404

    player = PlayerTable(id=1, first_name='Test', last_name='Player', nationality='USA', hand='U')
    db_client.session.add(player)
    db_client.session.commit()
    db_client.session.refresh(player)

    response = client.get(f'/player/{player.id}')
    assert response.status_code == 200
    # ensure response json matches expected schema
    PlayerSchema(**response.json())
    assert response.json()['name'] == player.name


def test_read_tournament_by_id(client, db_client):
    response = client.get('/tournament/1')
    assert response.status_code == 404

    tournament = TournamentTable(id='hi', name='Test', surface='Grass', draw_size=32,
                                 level='wta', start_date=datetime.now())
    db_client.session.add(tournament)
    db_client.session.commit()
    db_client.session.refresh(tournament)

    response = client.get(f'/tournament/{tournament.id}')
    assert response.status_code == 200
    # ensure response json matches expected schema
    TournamentSchema(**response.json())
    assert response.json()['name'] == tournament.name


def test_read_game_by_id(client, db_client):
    response = client.get('/game/1')
    assert response.status_code == 404

    tournament_id = db_client.session.query(TournamentTable).\
        filter(TournamentTable.name == 'Test').one().id

    game = GameTable(id=f'{tournament_id}_100', tournament_id=tournament_id,
                     round='R32', score='6-0 6-0', circuit=WTA_IDENTIFIER)
    db_client.session.add(game)
    db_client.session.commit()
    db_client.session.refresh(game)

    response = client.get(f'/game/{game.id}')
    assert response.status_code == 200
    # ensure response json matches expected schema
    GameSchema(**response.json())

    assert response.json()['tournament']['id'] == tournament_id
    assert response.json()['round'] == game.round
