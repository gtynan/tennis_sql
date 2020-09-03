from typing import Tuple
import pandas as pd
from datetime import datetime

from .db.models.player import Player


def format_player(row: object, fname: str = 'X', lname: str = 'X.1', nationality: str = 'UNK', dob: str = '19000000', hand: str = 'U') -> Player:
    """Given row from jeff sackmans player csv formats to player objetc

    Args:
        row (object): DataFrame row 
        fname (str, optional): column containing first name. Defaults to 'X'.
        lname (str, optional): column containing last name. Defaults to 'X.1'.
        nationality (str, optional): column containing nationality. Defaults to 'UNK'.
        dob (str, optional): column containing date of birth. Defaults to '19000000'.
        hand (str, optional): column containing hand. Defaults to 'U'.

    Returns:
        Player: player instance
    """
    return Player(first_name=row[fname],
                  last_name=row[lname],
                  nationality=row[nationality],
                  dob=datetime.strptime(str(row[dob]), '%Y%m%d'),
                  hand=row[hand])
