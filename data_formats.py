"""
資料格式：課程、學生、教室、選課紀錄、活動、活動報名紀錄的欄位，以及空的 db。
只定義欄位，不檢查資料、不讀寫檔案。
"""

from dataclasses import dataclass


@dataclass
class Course:
    """一門課程。"""

    course_id: str
    course_name: str
    credit: int
    is_required: bool
    instructor: str
    students_limit: int
    classroom: str
    schedule: dict[str, list[int]]  # {星期 "1"～"7": [節次 1～12]}，a、b、c 存成 10、11、12


@dataclass
class Student:
    """一位學生（已選課程從 db["enrollments"] 計算，報名的活動從 db["signups"] 計算）。"""

    student_id: str
    name: str
    major: str
    credit_limit: int = 24


@dataclass
class Classroom:
    """一間教室。"""

    classroom_id: str
    capacity: int
    equipment: list[str]
    building: str


@dataclass
class Enrollment:
    """一筆選課紀錄：哪位學生選了哪門課。"""

    student_id: str
    course_id: str


@dataclass
class Activity:
    """一項校園活動（只辦一次，在某一天）。"""

    activity_id: str
    activity_name: str
    date: str  # "2026-11-05"
    start_time: str  # "18:30"
    end_time: str  # "20:00"
    people_limit: int  # 預計人數，也是報名人數上限
    activity_type: str  # 講座、社團、讀書會、比賽、其他
    equipment: list[str]  # 場地需要的設備，例如 ["投影機", "麥克風"]，不需要時是 []
    classroom: str


@dataclass
class Signup:
    """一筆活動報名紀錄：哪位學生報名了哪項活動。"""

    student_id: str
    activity_id: str


def empty_db() -> dict:
    """建立一個空的 db。

    參數：
        無

    回傳：
        {"courses": {}, "students": {}, "classrooms": {}, "enrollments": [], "activities": {}, "signups": []}

    例子：
        db = empty_db()

    對應需求：資料格式
    """
    return {
        "courses": {},
        "students": {},
        "classrooms": {},
        "enrollments": [],
        "activities": {},
        "signups": [],
    }
