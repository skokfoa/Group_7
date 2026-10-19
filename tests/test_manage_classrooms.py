from data_formats import Classroom, Course, empty_db
from manage_classrooms import delete_classroom


def test_delete_classroom_in_use():
    db = empty_db()
    db["classrooms"]["EN201"] = Classroom("EN201", 60, ["投影機"], "綜合科館")
    db["classrooms"]["EN202"] = Classroom("EN202", 40, ["電腦"], "綜合科館")
    db["courses"]["CS101"] = Course("CS101", "計算機概論", 3, True, "王老師", 60, "EN201", {"1": [1, 2]})
    assert delete_classroom(db, "EN201") == ["EN201 還有課程使用，不能刪除"]
    assert "EN201" in db["classrooms"]
    assert db["courses"]["CS101"].classroom == "EN201"
