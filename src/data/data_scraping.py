from typing import Iterator, Tuple
import pandas as pd
import requests

from ..constants import PLAYER_URL, WTA_URL, ITF_URL, SOURCE_COL


def get_raw_players(n_players: int = None) -> pd.DataFrame:
    '''
    Gets all WTA players in Jeff Sackmans WTA data

    args:
        n_players: (ignore just used for testing) Number of players to return

    returns:
        dataframe of players
    '''
    return pd.read_csv(
        PLAYER_URL,
        mangle_dupe_cols=True,  # duplicate columns i.e. X, X -> X, X.1
        nrows=n_players,
        encoding="ISO-8859-1"
    )


def get_raw_games(year_from: int, year_to: int, n_games: int = None) -> pd.DataFrame:
    '''
    Gets all WTA and ITF games

    args:
        n_games: (ignore just used for testing) returns most recent WTA matches

    returns:
        raw dataframe of games
    '''
    if n_games:
        data = pd.read_csv(WTA_URL.format(year_to), encoding="ISO-8859-1", nrows=n_games)
        data[SOURCE_COL] = 'W'
        return data
    else:
        data = None
        for year in range(year_from, year_to + 1):
            new_wta = pd.read_csv(WTA_URL.format(year), encoding="ISO-8859-1")
            new_itf = pd.read_csv(ITF_URL.format(year), encoding="ISO-8859-1")

            new_wta[SOURCE_COL] = 'W'
            new_itf[SOURCE_COL] = 'I'

            if isinstance(data, pd.DataFrame):
                data = data.append(new_wta, ignore_index=True)
            else:
                data = new_wta

            data = data.append(new_itf, ignore_index=True)
        return data


def get_last_commit_sha() -> str:
    """Gets the SHA for the last github commit to the tennis_wta repo

    Raises:
        Exception: if request fails

    Returns:
        str: SHA
    """
    r = requests.get('https://api.github.com/repos/JeffSackmann/tennis_wta/commits')
    if r.status_code == 200:
        return r.json()[0]['sha']
    raise Exception("Get last commit failed.")


def get_file_changes(sha: str, previous_sha: str) -> Iterator[Tuple[str, str]]:
    """Given two SHA's returns filename and differences to file since previous SHA

    Args:
        sha (str): SHA for last commit to repo
        previous_sha (str): previous SHA to see which changes have happend since this commit

    Raises:
        Exception: if request fails

    Yields:
        Iterator[Tuple[str, str]]: (file_name, file_changes)
    """
    if previous_sha:
        r = requests.get(f'https://api.github.com/repos/jeffsackmann/tennis_wta/compare/{previous_sha}...{sha}')
    if r.status_code == 200:
        for file in r.json()['files']:
            try:
                yield file['filename'], file['patch']
            # when file has no `patch`
            except:
                pass
    else:
        raise Exception("Get files changed failed")
