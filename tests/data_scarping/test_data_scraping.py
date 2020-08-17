import pytest
import pandas as pd

from src.data_scraping.data_scraping import get_raw_players


def test_get_raw_players():
    raw_players = get_raw_players(n_players=5)
    assert len(raw_players) == 5
    assert isinstance(raw_players, pd.DataFrame)
