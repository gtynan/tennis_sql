import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.data.data_scraping import get_file_changes
from src.data.data_cleaning import to_datetime, raw_changes_to_df, clean_file_changes
from src.constants import SOURCE_COL, WTA_IDENTIFIER


def test_to_datetime():
    # ensure correctly formats date
    assert to_datetime(20200101) == datetime(2020, 1, 1)
    # ensure if date given date returned
    assert to_datetime(datetime(2020, 1, 1)) == datetime(2020, 1, 1)
    # ensure handles series
    pd.testing.assert_series_equal(to_datetime(pd.Series([20000101, 19901009])),
                                   pd.Series([datetime(2000, 1, 1), datetime(1990, 10, 9)]))

    # ensure handles None and nans
    assert to_datetime(None) is None
    assert to_datetime(np.nan) is None


def test_raw_changes_to_df():
    changes = "@@ -150, 133 + 150, 133 @ @ tourney_id, tourney_name, surface, draw_size, tourney_level, tourney_date, match_num, w\n 2020-1050, Hobart, Hard, 32, I, 20200113, 272, 214263, , , Catherine Cartan Bellis, R, , USA, 20.7665982204, 213631, , , Marie Bouzkova, R, , CZE, 21.4811772758, 3-6 7-6(4) 6-3, 3, R32, 170, 1, 3, 98, 63, 39, 12, 14, 9, 16, 2, 1, 119, 76, 45, 16, 16, 10, 18, 838, 20, 59, 979\n-1998-W-WT-NED-01A-1998,'s-Hertogenbosch,Grass,30,W,19980615,1,200660,,,Kimberly Po Messerli,R,,USA,26.6529774127,200745,,,Andrea Glass,R,,GER,21.9110198494,7-5 7-6,3,R32,,,,,,,,,,,,,,,,,,,,61,430,66,408\n+1998-W-WT-NED-01A-1998,s Hertogenbosch,Grass,30,W,19980615,1,200660,,,Kimberly Po Messerli,R,,USA,26.6529774127,200745,,,Andrea Glass,R,,GER,21.9110198494,7-5 7-6,3,R32,,,,,,,,,,,,,,,,,,,,61,430,66,408"
    df = raw_changes_to_df(changes, None)

    assert len(df) == 2
    assert isinstance(df, pd.DataFrame)

    # raw changes lines start with 1 of (' ' -  +) assert that is removed
    initial_values = [col_1[0] for col_1 in df.loc[:, 0].values]
    assert ~np.isin([' ', '-', '+'], initial_values).all()


def test_clean_file_changes():
    file_changes = get_file_changes('ca6476a75d180758723ac892c56bf334343053ab',
                                    'c6b74fbccd7a0eae5604a2a9e06da2e3d79a2c65')

    player_data, game_data = clean_file_changes(file_changes, None, None)

    # within this update only wta games were updated, no ITF or players
    assert player_data is None
    assert isinstance(game_data, pd.DataFrame)
    assert all(game_data[SOURCE_COL] == WTA_IDENTIFIER)
