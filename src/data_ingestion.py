from typing import Union
import pandas as pd
from sqlalchemy.orm import Session

from .db.db import DBClient, CommandDB, QueryDB
from .data_formatting import format_tournament, format_game
from .data_cleaning import infer_dob, to_datetime


def add_game(command_db: CommandDB, query_db, game: pd.Series) -> None:
    w_player = query_db.get_player(game['winner_name'],
                                   game['winner_age'])
    l_player = query_db.get_player(game['loser_name'],
                                   game['loser_age'])

    # players are added seperately if they are not present game will not be added
    assert (w_player is not None) & (l_player is not None)

    tournament = query_db.get_tournament(game['tourney_name'],
                                         game['tourney_date'])

    if tournament is None:
        tournament = format_tournament(game)

    f_game = format_game(game, tournament, w_player, l_player)

    command_db.add_game(f_game)


def add_games(session: Session, games: Union[pd.DataFrame, pd.Series]) -> None:
    command_db = CommandDB(session)
    query_db = QueryDB(session)

    games = games.copy(deep=True)

    # data cleaning
    games['tourney_date'] = to_datetime(games['tourney_date'])
    games['winner_age'] = infer_dob('winner_age', 'tourney_date', games)
    games['loser_age'] = infer_dob('loser_age', 'tourney_date', games)

    try:
        for _, game in games.iterrows():
            add_game(command_db, query_db, game)
    except AttributeError:
        add_game(command_db, query_db, games)
