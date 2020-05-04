import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)

from soccer_data import format_date, club_colors


def test_format_date():
    # it should apply USD formatting
    assert format_date("2019-08-11T13:45:00Z") == "2019-08-11"

def test_club_colors():

    assert club_colors("65") == "#1CC6E8"





