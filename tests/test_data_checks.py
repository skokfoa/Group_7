from data_checks import check_course, check_student
from data_formats import Course, Student, Classroom, empty_db


def test_check_course_valid():
    db = empty_db()
    db["classrooms"]["EN201"] = Classroom("EN201", 60, ["投影機"], "綜合科館")
    course = Course("CS101", "計算機概論", 3, True, "李老師", 60, "EN201", {"1": [1, 2]})
    assert check_course(db, course, True) == []


def test_check_course_multiple_errors():
    db = empty_db()
    db["classrooms"]["EN201"] = Classroom("EN201", 60, ["投影機"], "綜合科館")
    db["courses"]["CS102"] = Course("CS102", "演算法", 3, True, "王老師", 50, "EN201", {"2": [3, 4]})
    course = Course("CS102", "演算法", "abc", True, "王老師", 50, "EN201", {"2": [13]})
    assert check_course(db, course, True) == [
        "課程代號已存在：CS102",
        "學分必須為正整數：abc",
        "節次不合法：13",
    ]


def test_check_student_invalid_id():
    db = empty_db()
    student = Student("S01", "王小明", "資工一")
    assert check_student(db, student, True) == ["學號格式錯誤：S01"]
