from data_formats import Course
from timetable import build_timetable, search_timetable, find_free_slots, timetable_stats


def make_courses():
    return [
        Course("CS101", "計算機概論", 3, True, "李老師", 60, "EN201", {"1": [1, 2], "3": [1, 2]}),
        Course("MA101", "微積分", 3, True, "王老師", 50, "EN201", {"1": [5, 6]}),
        Course("PE101", "體育", 1, True, "林老師", 30, "EN202", {"2": [11, 12]}),
    ]


def test_build_timetable_size():
    table = build_timetable([])
    assert len(table) == 7
    assert all(row == [""] * 12 for row in table)


def test_course_shows_in_every_slot():
    table = build_timetable(make_courses())
    assert table[0][0] == "CS101"
    assert table[0][1] == "CS101"
    assert table[2][0] == "CS101"
    assert table[2][1] == "CS101"
    assert table[1][10] == "PE101"
    assert table[1][11] == "PE101"


def test_same_day_two_courses():
    table = build_timetable(make_courses())
    assert search_timetable(table, day="1") == [
        ("1", 1, "CS101"), ("1", 2, "CS101"), ("1", 5, "MA101"), ("1", 6, "MA101"),
    ]


def test_search_by_course_and_period():
    table = build_timetable(make_courses())
    assert search_timetable(table, course_id="CS101") == [
        ("1", 1, "CS101"), ("1", 2, "CS101"), ("3", 1, "CS101"), ("3", 2, "CS101"),
    ]
    assert search_timetable(table, period=1) == [("1", 1, "CS101"), ("3", 1, "CS101")]
    assert search_timetable(table, course_id="XX999") == []


def test_free_slots_three_in_a_row():
    table = build_timetable(make_courses())
    # 星期一第 3、4 節只有 2 節，不算；第 7～9 節剛好 3 節
    assert find_free_slots(table, ["1"], 1, 9, 3) == [("1", 7, 9)]


def test_free_slots_across_days():
    table = build_timetable(make_courses())
    assert find_free_slots(table, ["1", "2", "3"], 1, 4, 2) == [
        ("1", 3, 4), ("2", 1, 4), ("3", 3, 4),
    ]


def test_free_slots_none():
    table = build_timetable(make_courses())
    assert find_free_slots(table, ["1"], 1, 2, 1) == []


def test_timetable_stats():
    stats = timetable_stats(make_courses())
    assert stats["daily"] == {"1": 4, "2": 2, "3": 2, "4": 0, "5": 0, "6": 0, "7": 0}
    assert stats["credits"] == 7
    assert stats["gaps"] == 2
