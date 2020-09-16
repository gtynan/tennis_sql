from typing import Optional, Tuple
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from datetime import datetime

from arq import cron
from arq.connections import RedisSettings

from .data.data_scraping import get_last_commit_sha, get_file_changes, get_raw_players, get_raw_games
from .data.data_cleaning import to_datetime, raw_changes_to_df
from .data.data_formatting import format_player, raw_game_to_instances

from .db.db import QueryDB, CommandDB, DBClient

from .db.models.orm.player import Player
from .db.models.orm.tournament import Tournament
from .db.models.orm.game import Game
from .db.models.orm.performance import WPerformance, LPerformance

from .constants import SOURCE_COL, WTA_IDENTIFIER, ITF_IDENTIFIER


def add_player_data(command_db: CommandDB, player_data: pd.DataFrame, bulk: bool = False) -> None:
    player_data = player_data.apply(lambda player_row: format_player(player_row), axis=1).values
    command_db.ingest_objects(np.unique(player_data), Player, bulk=bulk)


def add_game_data(command_db: CommandDB, game_data: pd.DataFrame, bulk: bool = False) -> None:
    game_data = game_data.rename(columns={'winner_id': 'w_id', 'loser_id': 'l_id'})

    formatted_game_data = game_data.apply(
        lambda game_row: raw_game_to_instances(game_row), axis=1, result_type='expand').values

    tournaments, games, w_performances, l_performances = (formatted_game_data[:, 0],
                                                          formatted_game_data[:, 1], formatted_game_data[:, 2], formatted_game_data[:, 3])

    command_db.ingest_objects(np.unique(tournaments), Tournament, bulk=bulk)
    command_db.ingest_objects(np.unique(games), Game, bulk=bulk)
    command_db.ingest_objects(np.unique(w_performances), WPerformance, bulk=bulk)
    command_db.ingest_objects(np.unique(l_performances), LPerformance, bulk=bulk)


def get_updated_data(github_sha: str, db_sha: str) -> Tuple[pd.DataFrame]:
    player_data, game_data = None, None
    player_cols = get_raw_players(n_players=1).columns
    game_cols = get_raw_games(n_games=1, year_from=2020, year_to=2020).columns

    for file_name, raw_data in get_file_changes(github_sha, db_sha):
        if 'players' in file_name:
            # player data, will only ever appear once as an update hence no append
            player_data = raw_changes_to_df(raw_data, columns=player_cols)
            # back to for loop start as not adding game
            continue
        new_games = raw_changes_to_df(raw_data, columns=game_cols)
        if 'itf' in file_name:
            new_games[SOURCE_COL] = ITF_IDENTIFIER
        else:
            new_games[SOURCE_COL] = WTA_IDENTIFIER

        if game_data is None:
            game_data = new_games
        else:
            game_data = game_data.append(new_games, ignore_index=True)
    return player_data, game_data


async def ingest_data(ctx, year_from: int = 1967, year_to: int = datetime.now().year):
    db_client = DBClient()
    db_client.generate_schema()

    command_db, query_db = CommandDB(db_client.session), QueryDB(db_client.session)
    github_sha, last_ingested_sha = get_last_commit_sha(), query_db.get_last_ingested_sha()

    # nothing ingested yet (i.e. first run)
    if last_ingested_sha is None:
        # clear before bulk adding to avoid any conflicts
        db_client.clear_db_values()

        player_data = get_raw_players()
        add_player_data(command_db, player_data, bulk=True)

        game_data = get_raw_games(year_from, year_to)
        add_game_data(command_db, game_data, bulk=True)
    # github updated
    elif last_ingested_sha and (last_ingested_sha != github_sha):
        player_data, game_data = get_updated_data(github_sha, last_ingested_sha)
        add_player_data(command_db, player_data, bulk=False)
        add_game_data(command_db, game_data, bulk=False)
    # github not updated do nothin
    else:
        return
    command_db.add_last_ingested_sha(github_sha)


class WorkerSettings:
    redis_settings = RedisSettings()
    cron_jobs = [
        # will run once daily
        cron(ingest_data, hour=0, minute=0, second=0,  run_at_startup=True)
    ]
