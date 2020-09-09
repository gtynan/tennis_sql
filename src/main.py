from typing import Generator
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session

from .db.schema.player import PlayerSchema
from .db.schema.tournament import TournamentSchema
from .db.schema.game import GameSchema
from .db.db import DBClient, QueryDB

DBClient().generate_schema()
app = FastAPI()


# dependency
def get_query_db() -> Generator[QueryDB, None, None]:
    db = DBClient()
    try:
        yield QueryDB(db.session)
    finally:
        db.session.close()


@app.get('/player/{player_id}', response_model=PlayerSchema)
def read_player_by_id(player_id: int, db: QueryDB = Depends(get_query_db)):
    player = db.get_player_by_id(player_id)
    if player is None:
        raise HTTPException(status_code=404, detail='Player not found')
    return player


@app.get('/tournament/{tourney_id}', response_model=TournamentSchema)
def read_tournament_by_id(tourney_id: int, db: QueryDB = Depends(get_query_db)):
    tournament = db.get_tournament_by_id(tourney_id)
    if tournament is None:
        raise HTTPException(status_code=404, detail='Tournament not found')
    return tournament


@app.get('/game/{game_id}', response_model=GameSchema)
def read_game_by_id(game_id: int, db: QueryDB = Depends(get_query_db)):
    game = db.get_game_by_id(game_id)
    if game is None:
        raise HTTPException(status_code=404, detail='Game not found')
    return game
