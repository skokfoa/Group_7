from data_formats import Activity, Classroom, Course, Enrollment, Signup, Student, empty_db
from manage_activities import (
    activity_schedule, add_activity, update_activity, cancel_activity, get_activity, list_activities,
    classroom_problems, find_classrooms, count_signups, signed_up_activities, sign_up,
)


def make_db():
    db = empty_db()
    db["classrooms"]["EN201"] = Classroom("EN201", 60, ["投影機"], "綜合科館")
    db["classrooms"]["EN202"] = Classroom("EN202", 40, ["投影機", "麥克風"], "綜合科館")
    db["students"]["S001"] = Student("S001", "王小明", "資工一")
    db["students"]["S002"] = Student("S002", "李小華", "資工一")
    db["courses"]["CS205"] = Course("CS205", "資料結構", 3, True, "李老師", 60, "EN201", {"4": [11, 12]})
    db["enrollments"].append(Enrollment("S001", "CS205"))
    # 2026-11-05 是星期四，18:30～20:00 是第 11、12 節
    db["activities"]["A001"] = Activity("A001", "程式設計讀書會", "2026-11-05", "18:30", "20:00", 1, "讀書會", [], "EN202")
    return db


def new_activity(people=20, equipment=None, date="2026-11-05", start="18:30", end="20:00", classroom="EN202"):
    return Activity("A002", "期中說明會", date, start, end, people, "講座", equipment or [], classroom)


def test_activity_schedule():
    assert activity_schedule("2026-11-05", "18:30", "20:00") == {"4": [11, 12]}
    assert activity_schedule("2026-11-02", "12:00", "13:00") == {"1": [5]}


def test_activity_schedule_boundary():
    # 剛好是一節的頭尾
    assert activity_schedule("2026-11-07", "08:10", "09:00") == {"6": [1]}
    # 在兩節之間的下課時間，一節都沒佔用
    assert activity_schedule("2026-11-07", "09:00", "09:10") == {}
    # 整天
    assert activity_schedule("2026-11-08", "08:10", "20:00") == {"7": list(range(1, 13))}


def test_add_and_get_activity():
    db = make_db()
    activity = new_activity(date="2026-11-06")
    assert add_activity(db, activity) == []
    assert get_activity(db, "A002") == activity
    assert get_activity(db, "A999") is None
    assert add_activity(db, activity) == ["活動代號已存在：A002"]


def test_add_activity_lists_all_room_problems():
    db = make_db()
    activity = new_activity(people=80, equipment=["投影機", "麥克風"], classroom="EN201")
    assert add_activity(db, activity) == [
        "容量不足：EN201 可坐 60 人，活動預計 80 人",
        "缺少設備：EN201 沒有 麥克風",
        "教室衝堂：星期四第 b、c 節，EN201 已有課程 CS205 資料結構",
    ]
    assert "A002" not in db["activities"]


def test_room_conflict_with_activity_only_same_day():
    db = make_db()
    # 和 A001 同一天、同教室，第 12 節重疊
    assert add_activity(db, new_activity(start="19:10")) == ["教室衝堂：星期四第 c 節，EN202 已有活動 A001 程式設計讀書會"]
    # 下一週的星期四，同樣時間不算衝突
    assert add_activity(db, new_activity(date="2026-11-12")) == []


def test_room_capacity_exactly_enough():
    db = make_db()
    assert classroom_problems(db, new_activity(people=40, date="2026-11-06"), "EN202") == []
    assert classroom_problems(db, new_activity(people=41, date="2026-11-06"), "EN202") == ["容量不足：EN202 可坐 40 人，活動預計 41 人"]


def test_update_activity():
    db = make_db()
    changed = Activity("A001", "程式設計讀書會", "2026-11-05", "18:30", "20:00", 30, "讀書會", [], "EN202")
    # 和修改前的自己同時段，不算衝突
    assert update_activity(db, changed) == []
    assert get_activity(db, "A001").people_limit == 30
    missing = Activity("A999", "期末說明會", "2026-12-20", "10:00", "12:00", 30, "講座", [], "EN201")
    assert update_activity(db, missing) == ["找不到活動：A999"]


def test_cancel_activity_removes_signups():
    db = make_db()
    db["signups"].append(Signup("S002", "A001"))
    assert cancel_activity(db, "A001") == []
    assert "A001" not in db["activities"]
    assert db["signups"] == []
    assert cancel_activity(db, "A001") == ["找不到活動：A001"]


def test_list_activities_sorted():
    db = make_db()
    db["activities"]["A003"] = Activity("A003", "吉他社迎新", "2026-11-02", "18:10", "19:00", 30, "社團", [], "EN201")
    db["activities"]["A004"] = Activity("A004", "職涯講座", "2026-11-05", "12:10", "13:00", 30, "講座", [], "EN201")
    assert [a.activity_id for a in list_activities(db)] == ["A003", "A004", "A001"]
    assert list_activities(empty_db()) == []


def test_find_classrooms():
    db = make_db()
    # 下一週星期四晚上：EN201 有 CS205，EN202 沒人用
    found = find_classrooms(db, new_activity(equipment=["投影機"], date="2026-11-12", classroom=""))
    assert [room.classroom_id for room in found] == ["EN202"]
    assert find_classrooms(db, new_activity(people=500, classroom="")) == []


def test_sign_up_and_count():
    db = make_db()
    assert sign_up(db, "S002", "A001") == []
    assert count_signups(db, "A001") == 1
    assert signed_up_activities(db, "S002") == [db["activities"]["A001"]]
    assert signed_up_activities(db, "S999") == []


def test_sign_up_lists_all_problems():
    db = make_db()
    assert sign_up(db, "S002", "A001") == []
    # S001 星期四第 11、12 節有 CS205，而且 A001 只收 1 人
    assert sign_up(db, "S001", "A001") == [
        "衝堂：星期四第 b、c 節，已選課程 CS205 資料結構",
        "活動已額滿：1/1",
    ]
    assert count_signups(db, "A001") == 1


def test_sign_up_conflicts_with_activity():
    db = make_db()
    db["activities"]["A003"] = Activity("A003", "吉他社迎新", "2026-11-05", "17:10", "19:00", 30, "社團", [], "EN201")
    assert sign_up(db, "S002", "A001") == []
    assert sign_up(db, "S002", "A003") == ["衝堂：星期四第 b 節，已報名活動 A001 程式設計讀書會"]


def test_sign_up_unknown_and_twice():
    db = make_db()
    assert sign_up(db, "S999", "A999") == ["找不到學生：S999", "找不到活動：A999"]
    assert sign_up(db, "S002", "A001") == []
    assert sign_up(db, "S002", "A001") == ["已報名這項活動：A001"]