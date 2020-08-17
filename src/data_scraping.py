import pandas as pd


def get_raw_players(n_players: int = None) -> pd.DataFrame:
    '''
    Gets all WTA players in Jeff Sackmans WTA data

    args:
        n_players: Number of players to return (leave None for all)

    returns:
        dataframe of players
    '''
    return pd.read_csv(
        "https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players.csv",
        nrows=n_players)
