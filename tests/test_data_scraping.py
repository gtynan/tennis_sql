import pytest
import pandas as pd
import numpy as np

from src.data_scraping import get_raw_players
from src.constants import player_csv_map


@pytest.mark.slow
def test_get_raw_players():
    raw_players = get_raw_players(n_players=5)
    assert len(raw_players) == 5
    assert isinstance(raw_players, pd.DataFrame)
    expected_columns = list(player_csv_map.values())
    assert np.isin(expected_columns, raw_players.columns).all()
