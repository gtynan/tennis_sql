import pytest
from datetime import date
from src.data_ingestion import _infer_dob


@pytest.mark.parametrize('age, t_date, dob',
                         [
                             (38.2778918549, date(2020, 1, 6), date(1981, 9, 26)),
                             (23.6167008898, date(2009, 2, 7), date(1985, 6, 27)),
                             (22.6830937714, date(1978, 12, 25), date(1956, 4, 19))
                         ])
def test_infer_dob(age, t_date, dob):
    assert _infer_dob(age, t_date) == dob
