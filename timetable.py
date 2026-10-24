"""
個人課表：把課程排成星期一到日 × 12 節的課表，查詢、找連續空堂、統計。
只用傳進來的課程清單，不讀 db、不 print。
"""

from data_formats import Course


def build_timetable(courses: list[Course]) -> list[list[str]]:
    """把課程排成 7 × 12 的課表。

    參數：
        courses：課程清單

    回傳：
        table[星期 - 1][節次 - 1] 是那一格的課程代號，沒課是 ""；共 7 列（星期一到日）、每列 12 格（第 1～12 節）

    例子：
        build_timetable([Course("CS101", ..., {"1": [1, 2]})])[0][:3] → ["CS101", "CS101", ""]
        build_timetable([]) → 7 列，每列 12 個 ""

    對應需求：F3
    """
    raise NotImplementedError


def search_timetable(
    table: list[list[str]],
    day: str | None = None,
    period: int | None = None,
    course_id: str | None = None,
) -> list[tuple[str, int, str]]:
    """依條件查詢課表中有課的格子；沒給的條件不篩選。

    參數：
        table：build_timetable 的課表
        day：星期 "1"～"7"
        period：節次 1～12
        course_id：課程代號

    回傳：
        符合條件的 (星期, 節次, 課程代號) 清單，依星期、節次排序

    例子（星期一第 1、2 節是 CS101）：
        search_timetable(table, day="1") → [("1", 1, "CS101"), ("1", 2, "CS101")]
        search_timetable(table, course_id="CS101", period=2) → [("1", 2, "CS101")]

    對應需求：F3
    """
    raise NotImplementedError


def find_free_slots(table: list[list[str]], days: list[str], first: int, last: int, length: int) -> list[tuple[str, int, int]]:
    """在指定星期和節次範圍內，找出至少連續 length 節的空堂。

    參數：
        table：build_timetable 的課表
        days：要找的星期，例如 ["1", "2"]
        first、last：節次範圍，包含頭尾
        length：至少連續幾節

    回傳：
        (星期, 開始節次, 結束節次) 清單，依星期、節次排序；每一段都取到範圍內最長

    例子（只有星期一第 1、2 節有課）：
        find_free_slots(table, ["1"], 1, 9, 3) → [("1", 3, 9)]
        find_free_slots(table, ["1", "2"], 1, 4, 3) → [("2", 1, 4)]

    對應需求：F3
    """
    raise NotImplementedError


def timetable_stats(courses: list[Course]) -> dict:
    """統計每天上課節數、每週總學分和空堂數。

    參數：
        courses：課程清單

    回傳：
        {"daily": {"1": 節數, ..., "7": 節數}, "credits": 總學分, "gaps": 空堂數}
        空堂是同一天第一節課和最後一節課之間沒課的節數

    例子（只有一門 3 學分的課，星期一第 1、2、5 節）：
        timetable_stats(courses) → {"daily": {"1": 3, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0}, "credits": 3, "gaps": 2}

    對應需求：F3
    """
    raise NotImplementedError
