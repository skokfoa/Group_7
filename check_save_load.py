import json
from pathlib import Path
from tempfile import TemporaryDirectory

import data_formats
import save_load


# 準備四種測試資料
db = data_formats.empty_db()

db["classrooms"]["EN201"] = data_formats.Classroom(
    classroom_id="EN201",
    capacity=60,
    equipment=["投影機", "白板"],
    building="工程館"
)

db["courses"]["CS101"] = data_formats.Course(
    course_id="CS101",
    course_name="計算機概論",
    credit=3,
    is_required=True,
    instructor="李老師",
    students_limit=60,
    classroom="EN201",
    schedule={"1": [1, 2]}
)

db["students"]["S001"] = data_formats.Student(
    student_id="S001",
    name="測試學生",
    major="資工一",
    credit_limit=24
)

db["enrollments"].append(
    data_formats.Enrollment(
        student_id="S001",
        course_id="CS101"
    )
)

# 暫存資料夾離開 with 區塊後會自動清除
with TemporaryDirectory() as temp_dir:
    folder = Path(temp_dir) / "test_data"

    save_load.save_data(db, str(folder))
    loaded_db = save_load.load_data(str(folder))

    # 檢查四種資料存檔後讀回來是否完全相同
    assert loaded_db == db, "存檔後讀回的資料不一致"
    print("通過：四種資料存檔後讀回完全相同")

    # 檢查 JSON 中的 ID 放置位置
    for group, id_field in [
        ("courses", "course_id"),
        ("students", "student_id"),
        ("classrooms", "classroom_id"),
    ]:
        with open(folder / f"{group}.json", encoding="utf-8") as file:
            saved = json.load(file)

        for record in saved[group].values():
            assert id_field not in record, f"{group} 內層不應包含 ID"

    print("通過：課程、學生、教室的 ID 格式正確")

    # 檢查中文是否直接保留在檔案裡
    course_text = (folder / "courses.json").read_text(encoding="utf-8")
    assert "計算機概論" in course_text, "中文沒有直接保留"
    print("通過：JSON 保留中文字")

    # 檢查空資料能否正常存取
    empty_db = data_formats.empty_db()
    save_load.save_data(empty_db, str(folder))
    assert save_load.load_data(str(folder)) == empty_db
    print("通過：空資料也能正常存取")

print("本次測試全部通過！")