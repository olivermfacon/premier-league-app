import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)

from soccer_data import format_date, match_info, divider, result_probs

def test_format_date():
    # it should apply the date formatting
    assert format_date("2019-08-11T13:45:00Z") == "2019-08-11"

    # it should apply the date formatting - using some more functions
    #assert format_date("2020-08-11T13:45:00Z") == "2020-08-11"


def test_result_probs():
    # it should check the results probability function
    assert result_probs([100,20,10],[100,10,10]) == [42,12,46]

    # it should check the results probability function for another set of numbers
    assert result_probs([20,10,5],[10,24,1]) == [30,49,21]
    
    # it should check the results probability function for another set of numbers
    assert result_probs([12,8,5],[10,15,0]) == [24,46,30]

def test_match_info():
    #it should return the following information about the completed game given 'match' variable. 'Match' variable was set to that the pytest doesn't have to request data from football-data API.

    match = {'score': {'winner': 'AWAY_TEAM'}, 'homeTeam': {'id': 67, 'name': 'Newcastle United FC'}, 'awayTeam': {'id': 57, 'name': 'Arsenal FC'}}
    assert match_info((match),"Arsenal")== ["Newcastle United FC", "ARSENAL FC", "LOSS"]

def test_divider():
    #it should return the divider/line
    assert divider() == "---------------------------------------------"
