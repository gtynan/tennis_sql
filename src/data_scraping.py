import pandas as pd


def get_raw_players(n_players: int = None) -> pd.DataFrame:
    '''
    Gets all WTA players in Jeff Sackmans WTA data

    args:
        n_players: (ignore just used for testing) Number of players to return 

    returns:
        dataframe of players
    '''
    return pd.read_csv(
        "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players.csv",
        mangle_dupe_cols=True,  # duplicate columns i.e. X, X -> X, X.1
        nrows=n_players)
