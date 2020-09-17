from typing import Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime

from arq import cron
from arq.connections import RedisSettings

from .data.data_scraping import get_last_commit_sha, get_file_changes, get_raw_players, get_raw_games
from .data.data_cleaning import clean_file_changes
from .data.data_formatting import format_player, raw_game_to_objects

from .db.db import QueryDB, CommandDB, DBClient

from .db.models.orm.player import Player
from .db.models.orm.tournament import Tournament
from .db.models.orm.game import Game
from .db.models.orm.performance import WPerformance, LPerformance

from .constants import INGEST_YEAR_FROM, INGEST_YEAR_TO


def add_player_data(command_db: CommandDB, player_data: pd.DataFrame, bulk: bool = False) -> None:
    player_data = player_data.apply(lambda player_row: format_player(player_row), axis=1).values
    command_db.ingest_objects(np.unique(player_data), Player, bulk=bulk)


def add_game_data(command_db: CommandDB, game_data: pd.DataFrame, bulk: bool = False) -> None:
    game_data = game_data.rename(columns={'winner_id': 'w_id', 'loser_id': 'l_id'})

    formatted_game_data = game_data.apply(
        lambda game_row: raw_game_to_objects(game_row), axis=1, result_type='expand').values

    tournaments, games, w_performances, l_performances = np.hsplit(formatted_game_data, 4)

    command_db.ingest_objects(np.unique(tournaments), Tournament, bulk=bulk)
    command_db.ingest_objects(np.unique(games), Game, bulk=bulk)
    command_db.ingest_objects(np.unique(w_performances), WPerformance, bulk=bulk)
    command_db.ingest_objects(np.unique(l_performances), LPerformance, bulk=bulk)


async def ingest_data(ctx, year_from: int = INGEST_YEAR_FROM, year_to: int = INGEST_YEAR_TO):  # datetime.now().year):
    db_client = DBClient()
    db_client.generate_schema()

    command_db, query_db = CommandDB(db_client.session), QueryDB(db_client.session)
    github_sha, last_ingested_sha = get_last_commit_sha(), query_db.get_last_ingested_sha()

    # nothing ingested yet (i.e. first run)
    if last_ingested_sha is None:
        # clear before bulk adding to avoid any conflicts
        db_client.clear_db()

        player_data = get_raw_players()
        add_player_data(command_db, player_data, bulk=True)

        game_data = get_raw_games(year_from, year_to)
        add_game_data(command_db, game_data, bulk=True)

    # github updated
    elif last_ingested_sha and (last_ingested_sha != github_sha):
        # getting columns
        player_cols = get_raw_players(n_players=1).columns
        game_cols = get_raw_games(n_games=1, year_from=2020, year_to=2020).columns

        raw_file_changes = get_file_changes(github_sha, last_ingested_sha)
        player_data, game_data = clean_file_changes(raw_file_changes, player_cols, game_cols)

        if player_data is not None:
            add_player_data(command_db, player_data, bulk=False)
        if game_data is not None:
            add_game_data(command_db, game_data, bulk=False)

    # github not updated do nothing
    else:
        return

    command_db.add_last_ingested_sha(github_sha)


class WorkerSettings:
    redis_settings = RedisSettings()
    cron_jobs = [
        # will run once daily
        cron(ingest_data, hour=0, minute=0, second=0,  run_at_startup=True)
    ]
