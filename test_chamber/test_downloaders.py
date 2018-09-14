import pytest
from downloaders import *
from hypothesis import given, reject
from hypothesis.strategies import integers

@given(integers(), integers(), integers())
def test_make_user_list_hypothesis(list_size, start_number, end_number):

    if list_size * 10 > abs(start_number - end_number):  # Make sure the range is much bigger than list size:
        try:
            l = make_user_list(list_size, start_number, end_number)
            assert len(l) == list_size
            assert len(set(l)) == len(l)
        except (ValueError, AssertionError):
            reject()


def test_make_user_list():
    l = make_user_list(5, 0, 5)
    for i in range(0, 5):
        assert i in l
    assert len(l) == 5

    l = make_user_list(4, 1, 5)
    for i in range(1, 5):
        assert i in l
    assert len(l) == 4
