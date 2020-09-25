from datetime import datetime

# scraping urls
PLAYER_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players.csv"
WTA_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_{}.csv"
ITF_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_qual_itf_{}.csv"

SOURCE_COL = 'source'

WTA_IDENTIFIER = 'WAT'
ITF_IDENTIFIER = 'ITF'

SCRAPING_HEADER = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
}

INGEST_YEAR_FROM = 1968
INGEST_YEAR_TO = datetime.now().year
