from typing import Union, overload, List
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import io


def infer_dob(age: str, t_date: str, data: Union[pd.Series, pd.DataFrame]) -> Union[pd.Series, datetime]:
    """Convert age as a decimal to date of birth using tournament start date

    Args:
        age (str):column containing player age in decimal form
        t_date (str): column containing tournament start date
        data (Union[pd.Series, pd.DataFrame]): data object

    Returns:
        Union[pd.Series, datetime]: inferred ages
    """
    return data[t_date] - ((data[age]*365.24).round(decimals=0)).astype('timedelta64[D]')


@overload
def to_datetime(date: Union[int, str]) -> datetime: ...
@overload
def to_datetime(date: pd.Series) -> pd.Series: ...


def to_datetime(date: Union[pd.Series, int, str]) -> Union[pd.Series, datetime]:
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
        return datetime.strptime(str(date), format)


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
    changes = [row[0] for row in rows]
    rows = [row[1:] for row in rows]

    # convert to dataframe
    df = pd.read_csv(io.StringIO('\n'.join(rows)), header=columns)

    df['updated'] = changes
    # rows denoted - are old rows who's values have been replaced with rows denoted as +
    df = df[df.updated != '-']
    df.loc[df.updated == '+', 'updated'] = True
    df.loc[df.updated != True, 'updated'] = False

    return df.reset_index(drop=True)
