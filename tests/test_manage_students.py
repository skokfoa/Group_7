from data_formats import Student, Enrollment, empty_db
from manage_students import delete_student


def test_delete_student():
    db = empty_db()
    db["students"]["S001"] = Student("S001", "王小明", "資工一")
    db["students"]["S002"] = Student("S002", "李小華", "資工二")
    db["enrollments"].append(Enrollment("S001", "CS101"))
    db["enrollments"].append(Enrollment("S001", "CS102"))
    db["enrollments"].append(Enrollment("S002", "CS101"))
    assert delete_student(db, "S001") == []
    assert "S001" not in db["students"]
    assert "S002" in db["students"]
    assert all(e.student_id != "S001" for e in db["enrollments"])
    assert db["enrollments"] == [Enrollment("S002", "CS101")]
