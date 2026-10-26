"""存檔與載入：data/ 的 JSON 檔和 db 互相轉換，是唯一會讀寫檔案的地方。"""

import json
from pathlib import Path
from dataclasses import asdict
import data_formats


def load_data(data_dir: str) -> dict:
    """讀取 data_dir 裡的 courses.json、students.json、classrooms.json、enrollments.json，組成 db。

    參數：
        data_dir：資料夾路徑，例如 "data"

    回傳：
        db

    例子：
        db = load_data("data")

    對應需求：F6
    """
    db = data_formats.empty_db()

    course_path = Path(data_dir) / "courses.json"
    with open(course_path, encoding="utf-8") as file:
        course_data = json.load(file)

    for course_id, course_info in course_data["courses"].items():
        course = data_formats.Course(
            course_id=course_id,
            **course_info
        )
        db["courses"][course_id] = course

    student_path = Path(data_dir) / "students.json"
    with open(student_path, encoding="utf-8") as file:
        student_data = json.load(file)

    for student_id, student_info in student_data["students"].items():
        student = data_formats.Student(
            student_id=student_id,
            **student_info
        )
        db["students"][student_id] = student

    classroom_path = Path(data_dir) / "classrooms.json"
    with open(classroom_path, encoding="utf-8") as file:
        classroom_data = json.load(file)

    for classroom_id, classroom_info in classroom_data["classrooms"].items():
        classroom = data_formats.Classroom(
            classroom_id=classroom_id,
            **classroom_info
        )
        db["classrooms"][classroom_id] = classroom

    enrollment_path = Path(data_dir) / "enrollments.json"
    with open(enrollment_path, encoding="utf-8") as file:
        enrollment_data = json.load(file)

    for enrollment_info in enrollment_data["enrollments"]:
        enrollment = data_formats.Enrollment(**enrollment_info)
        db["enrollments"].append(enrollment)
    return db


def save_data(db: dict, data_dir: str) -> None:
    """把 db 寫進 data_dir 的四個 JSON 檔。

    參數：
        db：全部資料
        data_dir：資料夾路徑，例如 "data"

    回傳：
        無

    例子：
        save_data(db, "data") 之後 load_data("data") → 得到和 db 一樣的資料

    對應需求：F6
    """
    folder = Path(data_dir)
    folder.mkdir(parents=True, exist_ok=True)

    courses = {}
    for course_id, course in db["courses"].items():
        course_info = asdict(course)
        course_info.pop("course_id")
        courses[course_id] = course_info

    students = {}
    for student_id, student in db["students"].items():
        student_info = asdict(student)
        student_info.pop("student_id")
        students[student_id] = student_info

    classrooms = {}
    for classroom_id, classroom in db["classrooms"].items():
        classroom_info = asdict(classroom)
        classroom_info.pop("classroom_id")
        classrooms[classroom_id] = classroom_info

    enrollments = []
    for enrollment in db["enrollments"]:
        enrollments.append(asdict(enrollment))

    files = {
        "courses.json": {"courses": courses},
        "students.json": {"students": students},
        "classrooms.json": {"classrooms": classrooms},
        "enrollments.json": {"enrollments": enrollments}
    }

    for filename, content in files.items():
        with open(folder / filename, "w", encoding="utf-8") as file:
            json.dump(content, file, ensure_ascii=False, indent=4)
