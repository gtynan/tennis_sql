import pytest
import pandas as pd
import numpy as np

from src.data_scraping import get_raw_players
from src.constants import player_csv_map


def test_get_raw_players(sample_players):
    raw_players = sample_players
    expected_columns = list(player_csv_map.values())

    assert len(raw_players) == 5
    assert isinstance(raw_players, pd.DataFrame)
    assert np.isin(expected_columns, raw_players.columns).all()
