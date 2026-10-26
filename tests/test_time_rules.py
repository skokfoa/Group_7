import pytest
from time_rules import period_to_number, is_valid_period


@pytest.mark.parametrize("text, expected", [
    ("1", 1), ("2", 2), ("3", 3), ("4", 4),
    ("5", 5), ("6", 6), ("7", 7), ("8", 8),
    ("9", 9), ("a", 10), ("b", 11), ("c", 12),
])
def test_period_to_number_valid(text, expected):
    assert period_to_number(text) == expected


@pytest.mark.parametrize("text", ["0", "13", "d", "x", "-1", ""])
def test_period_to_number_invalid(text):
    assert period_to_number(text) is None


@pytest.mark.parametrize("period, expected", [
    (1, True), (2, True), (3, True), (4, True),
    (5, True), (6, True), (7, True), (8, True),
    (9, True), (10, True), (11, True), (12, True),
    (0, False), (13, False), (-1, False),
])
def test_is_valid_period(period, expected):
    assert is_valid_period(period) is expected
