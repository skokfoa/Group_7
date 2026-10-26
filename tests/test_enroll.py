from data_formats import Course, Student, Classroom, Enrollment, empty_db
from enroll import enrolled_courses, total_credits, add_enrollment, drop_enrollment


def make_db():
    db = empty_db()
    db["classrooms"]["EN201"] = Classroom("EN201", 60, ["投影機"], "綜合科館")
    db["classrooms"]["EN202"] = Classroom("EN202", 40, ["電腦"], "綜合科館")
    db["students"]["S001"] = Student("S001", "王小明", "資工一")
    db["students"]["S002"] = Student("S002", "李小華", "資工一", 6)
    db["courses"]["MA101"] = Course("MA101", "微積分", 3, True, "王老師", 50, "EN201", {"2": [3, 4]})
    db["courses"]["CS101"] = Course("CS101", "計算機概論", 3, True, "李老師", 60, "EN201", {"1": [1, 2]})
    db["courses"]["CS102"] = Course("CS102", "Python 程式設計", 3, False, "陳老師", 1, "EN202", {"2": [3, 4], "4": [5]})
    db["courses"]["PE101"] = Course("PE101", "體育", 1, True, "林老師", 30, "EN201", {"4": [5]})
    db["enrollments"].append(Enrollment("S001", "MA101"))
    db["enrollments"].append(Enrollment("S001", "PE101"))
    return db


def test_enrolled_courses_and_credits():
    db = make_db()
    assert [course.course_id for course in enrolled_courses(db, "S001")] == ["MA101", "PE101"]
    assert total_credits(db, "S001") == 4
    assert enrolled_courses(db, "S999") == []


def test_add_enrollment_success():
    db = make_db()
    assert add_enrollment(db, "S001", "CS101") == []
    assert Enrollment("S001", "CS101") in db["enrollments"]


def test_add_enrollment_unknown_student_and_course():
    db = make_db()
    assert add_enrollment(db, "S999", "XX999") == ["找不到學生：S999", "找不到課程：XX999"]


def test_add_enrollment_already_enrolled():
    db = make_db()
    assert add_enrollment(db, "S001", "MA101") == ["已選過這門課：MA101"]
    assert len(db["enrollments"]) == 2


def test_add_enrollment_lists_all_conflicts_in_order():
    db = make_db()
    db["enrollments"].append(Enrollment("S002", "CS102"))
    # CS102 和 MA101（星期二）、PE101（星期四）都衝堂，而且已額滿
    assert add_enrollment(db, "S001", "CS102") == [
        "衝堂：星期二第 3、4 節，已選課程 MA101 微積分",
        "衝堂：星期四第 5 節，已選課程 PE101 體育",
        "課程已額滿：1/1",
    ]
    assert len(db["enrollments"]) == 3


def test_add_enrollment_over_credit_limit():
    db = make_db()
    db["enrollments"].append(Enrollment("S002", "CS101"))
    assert add_enrollment(db, "S002", "MA101") == []
    assert add_enrollment(db, "S002", "PE101") == ["學分超過上限：加選後 7 學分，上限 6"]


def test_add_enrollment_exactly_credit_limit():
    db = make_db()
    assert add_enrollment(db, "S002", "CS101") == []
    assert add_enrollment(db, "S002", "MA101") == []
    assert total_credits(db, "S002") == 6


def test_add_enrollment_room_conflict():
    db = make_db()
    db["courses"]["EE101"] = Course("EE101", "電路學", 3, True, "張老師", 50, "EN201", {"1": [2, 3]})
    assert add_enrollment(db, "S002", "EE101") == ["教室衝堂：星期一第 2 節，EN201 已有 CS101 計算機概論"]


def test_drop_enrollment():
    db = make_db()
    assert drop_enrollment(db, "S001", "MA101") == []
    assert Enrollment("S001", "MA101") not in db["enrollments"]
    assert drop_enrollment(db, "S001", "MA101") == ["沒有這筆選課紀錄：S001 MA101"]
