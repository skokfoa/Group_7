from data_formats import Course, Classroom, Enrollment, empty_db
from manage_courses import add_course, get_course, delete_course, cancel_course, search_courses


def test_add_and_get_course():
    db = empty_db()
    db["classrooms"]["EN201"] = Classroom("EN201", 60, ["投影機"], "綜合科館")
    course = Course("CS101", "計算機概論", 3, True, "李老師", 60, "EN201", {"1": [1, 2]})
    assert add_course(db, course) == []
    assert get_course(db, "CS101") == course


def test_delete_course_with_students():
    db = empty_db()
    db["courses"]["CS102"] = Course("CS102", "演算法", 3, True, "王老師", 50, "EN201", {"2": [3, 4]})
    db["enrollments"].append(Enrollment("S001", "CS102"))
    assert delete_course(db, "CS102") == ["CS102 已有學生選修，請改用取消課程"]
    assert "CS102" in db["courses"]
    assert len(db["enrollments"]) == 1


def test_cancel_course():
    db = empty_db()
    db["courses"]["CS102"] = Course("CS102", "演算法", 3, True, "王老師", 50, "EN201", {"2": [3, 4]})
    db["enrollments"].append(Enrollment("S001", "CS102"))
    db["enrollments"].append(Enrollment("S002", "CS102"))
    assert cancel_course(db, "CS102") == []
    assert "CS102" not in db["courses"]
    assert all(e.course_id != "CS102" for e in db["enrollments"])


def test_search_courses_by_instructor():
    db = empty_db()
    db["courses"]["CS101"] = Course("CS101", "計算機概論", 3, True, "王老師", 60, "EN201", {"1": [1, 2]})
    db["courses"]["CS102"] = Course("CS102", "演算法", 3, True, "李老師", 50, "EN201", {"2": [3, 4]})
    db["courses"]["CS103"] = Course("CS103", "資料結構", 3, True, "王老師", 50, "EN201", {"3": [5, 6]})
    result = search_courses(db, instructor="王老師")
    assert [course.course_id for course in result] == ["CS101", "CS103"]
