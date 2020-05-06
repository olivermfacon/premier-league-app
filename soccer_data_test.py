import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)
#import os
from soccer_data import format_date, club_colors, match_info, outcome, get_menu_option, divider, result_probs

#CI_ENV = os.environ.get("CI") == "true"

def test_format_date():
    # it should apply USD formatting
    assert format_date("2019-08-11T13:45:00Z") == "2019-08-11"


def test_result_probs():
    assert result_probs([100,20,10],[100,10,10]) == [42,12,46]


def test_match_info():
    match = {'score': {'winner': 'AWAY_TEAM'}, 'homeTeam': {'id': 67, 'name': 'Newcastle United FC'}, 'awayTeam': {'id': 57, 'name': 'Arsenal FC'}}
    assert match_info((match),"Arsenal")== ["Newcastle United FC", "ARSENAL FC", "LOSS"]

def test_divider():
    #it should return the divider/line
    assert divider() == "---------------------------------------------"
