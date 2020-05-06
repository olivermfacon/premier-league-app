import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)
#import os
from soccer_data import format_date, club_colors, match_info, outcome, get_menu_option

#CI_ENV = os.environ.get("CI") == "true"

def test_format_date():
    # it should apply USD formatting
    assert format_date("2019-08-11T13:45:00Z") == "2019-08-11"


def test_club_colors():

    assert club_colors("65") == ["#1CC6E8", "White"]

def test_outcome():
    assert outcome(.7) == "Given the probability of win, your team will most likely win."
    assert outcome(.5) == "Given the probability of win, your team will most likely draw."
    assert outcome(.2) == "Given the probability of win, your team will most likely lose."


#@pytest.mark.skipif(CI_ENV==True, reason="to avoid issuing HTTP requests on the CI server")
#def test_match_info():
    #home_Team = "ARSENAL FC"
    #match = {'score': {'winner': 'AWAY_TEAM', 'duration': 'REGULAR', 'fullTime': {'homeTeam': 0, 'awayTeam': 1}, 'homeTeam': {'id': 67, 'name': 'Newcastle United FC'}, 'awayTeam': {'id': 57, 'name': 'Arsenal FC'}}}
    #match_information = match_info(match)
    #assert match_information == ["Newcastle", 2]


