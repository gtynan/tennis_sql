import pytest
from src.db.db import QueryDB, CommandDB
from src.workers import get_latest_data
from src.db.schema.player import PlayerCreateSchema
from src.db.schema.tournament import TournamentCreateSchema
from src.db.schema.game import GameCreateSchema
from src.db.schema.performance import PerformanceCreateSchema


@pytest.mark.slow
def test_get_latest_data(db_client):
    # should scrape 1 years of data and all players
    players, tournaments, games, w_perfs, l_perfs = get_latest_data('', year_from=1968, year_to=1968)

    # ensure list objects all assumed type and length greater than 1 to ensure not just first object returning
    assert all([isinstance(player, PlayerCreateSchema) for player in players]) & (len(players) > 1)
    assert all([isinstance(tournament, TournamentCreateSchema) for tournament in tournaments]) & (len(tournaments) > 1)
    assert all([isinstance(game, GameCreateSchema) for game in games]) & (len(games) > 1)
    assert all([isinstance(w_perf, PerformanceCreateSchema) & (w_perf.won) for w_perf in w_perfs]) & (len(w_perfs) > 1)
    assert all([isinstance(l_perf, PerformanceCreateSchema) & (~l_perf.won) for l_perf in l_perfs]) & (len(l_perfs) > 1)

    # identical sha's should trigger no new data
    player, tournament, game, w_perf, l_perf = get_latest_data('a', 'a')

    assert player is None
    assert tournament is None
    assert game is None
    assert w_perf is None
    assert l_perf is None

    player, tournament, game, w_perf, l_perf = get_latest_data(
        'ca6476a75d180758723ac892c56bf334343053ab', 'c6b74fbccd7a0eae5604a2a9e06da2e3d79a2c65')

    assert player is None
    assert all([isinstance(tournament, TournamentCreateSchema) for tournament in tournaments]) & (len(tournaments) > 1)
    assert all([isinstance(game, GameCreateSchema) for game in games]) & (len(games) > 1)
    assert all([isinstance(w_perf, PerformanceCreateSchema) & (w_perf.won) for w_perf in w_perfs]) & (len(w_perfs) > 1)
    assert all([isinstance(l_perf, PerformanceCreateSchema) & (~l_perf.won) for l_perf in l_perfs]) & (len(l_perfs) > 1)
