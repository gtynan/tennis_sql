import pytest
import pandas as pd
from datetime import datetime
from src.data.data_cleaning import infer_dob, to_datetime


def test_infer_dob():
    age_col, t_date_col = 'age', 't_date'
    # dataframe of ages and tourney start dates
    data = pd.DataFrame(data=[[38.2778918549, datetime(2020, 1, 6)],
                              [23.6167008898, datetime(2009, 2, 7)],
                              [22.6830937714, datetime(1978, 12, 25)]],
                        columns=[age_col, t_date_col])
    # expected date of births
    e_dob = pd.Series([datetime(1981, 9, 26), datetime(1985, 6, 27),  datetime(1956, 4, 19)])

    dob = infer_dob(age_col, t_date_col, data)

    pd.testing.assert_series_equal(e_dob, dob)


def test_to_datetime():
    # ensure correctly formats date
    assert to_datetime(20200101) == datetime(2020, 1, 1)
    # ensure if date given date returned
    assert to_datetime(datetime(2020, 1, 1)) == datetime(2020, 1, 1)
    # ensure handles series
    pd.testing.assert_series_equal(to_datetime(pd.Series([20000101, 19901009])),
                                   pd.Series([datetime(2000, 1, 1), datetime(1990, 10, 9)]))
