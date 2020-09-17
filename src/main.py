from typing import Generator
from fastapi import FastAPI, Depends, HTTPException

from .db.db import DBClient, QueryDB
from .db.models.orm.player import Player as ORMPlayer
from .db.models.pydantic.player import Player
from .db.models.orm.tournament import Tournament as ORMTournament
from .db.models.pydantic.tournament import Tournament
from .db.models.orm.game import Game as ORMGame
from .db.models.pydantic.game import Game


app = FastAPI()


# dependency
def get_query_db() -> Generator[QueryDB, None, None]:
    db = DBClient()
    try:
        yield QueryDB(db.session)
    finally:
        db.session.close()


@app.get('/player/{player_id}', response_model=Player)
def read_player_by_id(player_id: int, db: QueryDB = Depends(get_query_db)):
    player = db.get_object_by_id(player_id, ORMPlayer)
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found')
    return player


@app.get('/tournament/{tourney_id}', response_model=Tournament)
def read_tournament_by_id(tourney_id: str, db: QueryDB = Depends(get_query_db)):
    tournament = db.get_object_by_id(tourney_id, ORMTournament)
    if tournament is None:
        raise HTTPException(status_code=404, detail='Tournament not found')
    return tournament


@app.get('/game/{game_id}', response_model=Game)
def read_game_by_id(game_id: str, db: QueryDB = Depends(get_query_db)):
    game = db.get_object_by_id(game_id, ORMGame)
    if game is None:
        raise HTTPException(status_code=404, detail='Game not found')
    return game
