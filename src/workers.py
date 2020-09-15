from typing import Optional, Tuple
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from datetime import datetime

from .data.data_scraping import get_last_commit_sha, get_file_changes, get_raw_players, get_raw_games
from .data.data_cleaning import to_datetime, raw_changes_to_df
from .data.data_formatting import format_player, raw_game_to_instances

from .db.db import QueryDB, CommandDB
from .db.schema.base import BaseModel
from .db.schema.player import PlayerCreateSchema, PlayerTable
from .constants import SOURCE_COL, WTA_IDENTIFIER, ITF_IDENTIFIER


def get_latest_data(github_sha: str, db_sha: Optional[str] = None, year_from: int = 1967, year_to: int = datetime.now().year) -> Tuple[BaseModel]:
    if db_sha:
        # get changes between last ingested sha and latest github sha
        if db_sha != github_sha:
            player_data, game_data = None, None
            player_cols = get_raw_players(n_players=1).columns
            game_cols = get_raw_games(n_games=1, year_from=year_to,
                                      year_to=year_to).columns

            for file_name, raw_data in get_file_changes(github_sha, db_sha):
                if 'players' in file_name:
                    # player data, will only ever appear once as an update hence no append
                    player_data = raw_changes_to_df(raw_data, columns=player_cols)
                    # back to for loop start as not adding game
                    continue

                new_games = raw_changes_to_df(raw_data, columns=game_cols)

                if 'itf' in file_name:
                    # itf match data
                    new_games[SOURCE_COL] = ITF_IDENTIFIER
                else:
                    # wta match data
                    new_games[SOURCE_COL] = WTA_IDENTIFIER

                print(new_games)

                if game_data is None:
                    game_data = new_games
                else:
                    game_data = game_data.append(new_games, ignore_index=True)

        # no updates to ingest
        else:
            return None, None, None, None, None
    # initial ingestion
    else:
        player_data = get_raw_players()
        game_data = get_raw_games(year_from, year_to)

    # format raw data
    if player_data is not None:
        player_data = player_data.apply(lambda player_row: format_player(player_row), axis=1).values

    if game_data is not None:
        game_data = game_data.rename(columns={'winner_id': 'w_id', 'loser_id': 'l_id'})
        game_data = game_data.apply(
            lambda game_row: raw_game_to_instances(game_row), axis=1, result_type='expand').values

    try:
        return player_data, game_data[:, 0], game_data[:, 1], game_data[:, 2], game_data[:, 3]
    except:
        try:
            return player_data, None, None, None, None
        except:
            return None, None, None, None, None
