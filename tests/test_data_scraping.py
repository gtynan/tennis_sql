import pytest
import pandas as pd
import numpy as np
from datetime import datetime

from src.data_scraping import get_raw_players, get_raw_games


@pytest.mark.slow
def test_get_raw_players():
    players = get_raw_players(n_players=5)

    assert len(players) == 5
    assert isinstance(players, pd.DataFrame)


@pytest.mark.slow
def test_get_raw_games():
    year = 2020
    games = get_raw_games(year, year, 5)

    assert len(games) == 5
    assert isinstance(games, pd.DataFrame)
    # ensure first and last row's date correct year
    assert datetime.strptime(str(games.loc[0, 'tourney_date']), '%Y%m%d').year == year
    assert datetime.strptime(str(games.loc[games.index[-1], 'tourney_date']), '%Y%m%d').year == year
