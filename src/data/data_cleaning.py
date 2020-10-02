from typing import Union, overload, List, Tuple, Iterator
import pandas as pd
import numpy as np
from datetime import datetime
import io

from ..constants import SOURCE_COL, WTA_IDENTIFIER, ITF_IDENTIFIER


@overload
def to_datetime(date: Union[int, str]) -> datetime: ...
@overload
def to_datetime(date: pd.Series) -> pd.Series: ...


def to_datetime(date: Union[pd.Series, int, float, str]) -> Union[pd.Series, datetime]:
    """Converts string to datetime

    Args:
        date (Union[str, int]): representation of date

    Returns:
        datetime: datetime representation
    """
    # expect date to be YYYYMMDD
    format = '%Y%m%d'

    if isinstance(date, pd.Series):
        return pd.to_datetime(date, format=format)
    else:
        if isinstance(date, datetime):
            return date
        try:
            return datetime.strptime(str(int(date)), format)
        except:
            return None


def raw_changes_to_df(raw_string: str, columns: List[str]) -> pd.DataFrame:
    """Given raw string of github changes convert to dataframe to be cleaned and inserted. Rows denoted as `updated` are old data with new values

    Args:
        raw_string (str): raw string of github changes
        columns (List[str]): columns to set on returned dataframe

    Returns:
        pd.DataFrame: string data in dataframe form
    """
    # ignore first row as just github flags
    rows = raw_string.split('\n')[1:]

    # can be one of ' ', -, +
    changes = np.array([row[0] for row in rows])
    rows = [row[1:] for row in rows]

    # convert to dataframe
    df = pd.read_csv(io.StringIO('\n'.join(rows)), names=columns, header=None)

    # rows denoted - are old rows who's values have been replaced with rows denoted as +
    df = df.loc[changes != '-']
    return df.reset_index(drop=True)


def clean_file_changes(file_changes: Iterator[Tuple[str, str]], player_cols: List[str], game_cols: List[str]):
    player_data, game_data = None, None

    for file_name, raw_data in file_changes:
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
