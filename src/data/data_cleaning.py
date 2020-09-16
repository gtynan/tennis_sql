from typing import Union, overload, List, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import io


def get_game_id(tournament_id: str, match_num: str) -> str:
    return f'{tournament_id}_{match_num}'


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
    format = '%Y%m%d'

    if isinstance(date, pd.Series):
        if isinstance(date.dtype, datetime):
            return date
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
