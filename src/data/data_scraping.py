from typing import Iterator, Tuple, Optional
import pandas as pd
import requests
from requests.exceptions import HTTPError
from io import StringIO

from ..constants import PLAYER_URL, SOURCE_COL, GAME_SOURCES, SCRAPING_HEADER
from ..logger import get_logger


logger = get_logger("data_scraping")


def get_raw_players() -> pd.DataFrame:
    """Gets all WTA players in Jeff Sackmans WTA data

    Returns:
        pd.DataFrame: player details dataframe
    """
    return pd.read_csv(
        PLAYER_URL,
        mangle_dupe_cols=True,  # duplicate columns i.e. X, X -> X, X.1
        encoding="ISO-8859-1",
    )


def get_raw_games(year: int) -> Optional[pd.DataFrame]:
    """Gets all games for specified year from GAME_SOURCES in constants.py

    Args:
        year (int): specified year to scrape game data

    Returns:
        Optional[pd.DataFrame]: all games for that year
    """
    data = None
    for identifier, url in GAME_SOURCES.items():
        try:
            # using requests rather than pandas so that we can add a header
            req = requests.get(url.format(year),
                               headers=SCRAPING_HEADER)
            # raises HttpError error if one
            req.raise_for_status()

            logger.info(f"GOT: {url.format(year)}")

            new_data = pd.read_csv(StringIO(req.text))
            new_data[SOURCE_COL] = identifier

            if data is None:
                data = new_data
            else:
                data = data.append(new_data, ignore_index=True)
        # file doesn't exist
        except HTTPError:
            logger.error(f'NOT FOUND: {url.format(year)}')
        # if either URL is None
        except AttributeError:
            logger.error(f"URL ATTRIBUTE ERROR: ensure URL not None")
    return data


def get_last_commit_sha() -> str:
    """Gets the SHA for the last github commit to the tennis_wta repo

    Raises:
        Exception: if request fails

    Returns:
        str: SHA
    """
    r = requests.get('https://api.github.com/repos/JeffSackmann/tennis_wta/commits',
                     headers=SCRAPING_HEADER)
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
    r = requests.get(f'https://api.github.com/repos/jeffsackmann/tennis_wta/compare/{previous_sha}...{sha}',
                     headers=SCRAPING_HEADER)
    if r.status_code == 200:
        for file in r.json()['files']:
            try:
                yield file['filename'], file['patch']  # patch contains all raw changes made
            # when file has no `patch` it means no changes were made
            except:
                pass
    else:
        raise Exception("Get files changed failed")
