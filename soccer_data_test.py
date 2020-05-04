import pytest # for pytest.raises (see: https://docs.pytest.org/en/latest/assert.html)

from soccer_data import format_date


def test_format_date():
    #adapted from https://github.com/s2t2/shopping-cart-screencast/blob/testing/shopping_cart_test.py
    # it should apply USD formatting
    assert format_date("2019-08-11T13:45:00Z") == "2019-08-11"


