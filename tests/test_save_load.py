from data_formats import Course, Student, Classroom, Enrollment, empty_db
from save_load import save_data, load_data


def test_save_and_load(tmp_path):
    db = empty_db()
    db["courses"]["CS101"] = Course("CS101", "計算機概論", 3, True, "王老師", 60, "EN201", {"1": [1, 2]})
    db["students"]["S001"] = Student("S001", "王小明", "資工一")
    db["classrooms"]["EN201"] = Classroom("EN201", 60, ["投影機"], "綜合科館")
    db["enrollments"].append(Enrollment("S001", "CS101"))
    save_data(db, str(tmp_path))
    for filename in ["courses.json", "students.json", "classrooms.json", "enrollments.json"]:
        assert (tmp_path / filename).is_file()
    loaded_db = load_data(str(tmp_path))
    assert loaded_db == db
