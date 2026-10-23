import pytest
from time_rules import (
    period_to_number, period_to_text, is_valid_day, is_valid_period,
    day_to_text, slot_text, find_conflicts,
)


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


@pytest.mark.parametrize("number, expected", [(1, "1"), (9, "9"), (10, "a"), (11, "b"), (12, "c")])
def test_period_to_text(number, expected):
    assert period_to_text(number) == expected


@pytest.mark.parametrize("day, expected", [
    ("1", True), ("7", True), ("0", False), ("8", False), ("", False), ("12", False),
])
def test_is_valid_day(day, expected):
    assert is_valid_day(day) is expected


def test_day_to_text():
    assert day_to_text("1") == "星期一"
    assert day_to_text("7") == "星期日"


def test_slot_text():
    assert slot_text("2", [3, 4]) == "星期二第 3、4 節"
    assert slot_text("5", [11]) == "星期五第 b 節"


def test_find_conflicts_overlap():
    a = {"2": [3, 4], "4": [5]}
    b = {"2": [4, 5], "4": [5]}
    assert find_conflicts(a, b) == {"2": [4], "4": [5]}


def test_find_conflicts_none():
    assert find_conflicts({"1": [1, 2]}, {"2": [1, 2]}) == {}
    assert find_conflicts({"1": [1, 2]}, {"1": [3, 4]}) == {}
