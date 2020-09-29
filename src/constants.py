from datetime import datetime

# scraping urls
PLAYER_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players.csv"

SCRAPING_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}

INGEST_YEAR_FROM = 1968
INGEST_YEAR_TO = datetime.now().year

GAME_SOURCES = {
    "WTA": "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_{}.csv",
    "ITF": "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_qual_itf_{}.csv",
}

SOURCE_COL = 'source'

"""
Map our column values to jeff sackman column values so we can extract required info
Format: our_column: jeff_column
"""

PLAYER_COLS = {
    "id": "200000",
    "first_name": "X",
    "last_name": "X.1",
    "nationality": "UNK",
    "dob": "19000000",
    "hand": "U",
}

TOURNAMENT_COLS = {
    "id": "tourney_id",
    "name": "tourney_name",
    "surface": "surface",
    "draw_size": "draw_size",
    "level": "tourney_level",
    "start_date": "tourney_date",
    "circuit": SOURCE_COL,
}

GAME_COLS = {
    "tournament_id": "tourney_id",
    "match_num": "match_num",
    "round": "round",
    "score": "score",
}

PERFORMANCE_COLS = {
    "player_id": "id",
    "aces": "ace",
    "double_faults": "df",
    "serve_points": "svpt",
    "first_serve_in": "1stIn",
    "first_serve_won": "1stWon",
    "second_serve_won": "2ndWon",
    "serve_games": "SvGms",
    "break_points_faced": "bpFaced",
    "break_points_saved": "bpSaved",
}
