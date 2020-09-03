import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


def _infer_dob(age: float, t_date: datetime) -> datetime:
    """Convert age as a decimal to date of birth using tournament start date

    Args:
        age (float): player's current age
        t_date (datetime): tournament start date

    Returns:
        datetime: player's dob
    """
    return t_date - relativedelta(days=age*365.24)
