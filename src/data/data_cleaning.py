from typing import Union, overload
import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


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
