"""
選課：加選、退選，以及學生已選的課程和學分。
加選時檢查所有條件、一次回報；不 print、不讀寫檔案。
"""

from data_formats import Course, Enrollment
import manage_courses
import time_rules


def enrolled_courses(db: dict, student_id: str) -> list[Course]:
    """列出一位學生已選的課程。

    參數：
        db：全部資料
        student_id：學號

    回傳：
        課程清單，依課程代號排序；沒有選課時是 []

    例子（S001 選了 MA101、CS102）：
        enrolled_courses(db, "S001") → [Course("CS102", ...), Course("MA101", ...)]
        enrolled_courses(db, "S999") → []

    對應需求：F2-01、F3
    """
    course_ids = []
    for enrollment in db["enrollments"]:
        if enrollment.student_id == student_id:
            course_ids.append(enrollment.course_id)
    course_ids.sort()

    courses = []
    for course_id in course_ids:
        courses.append(db["courses"][course_id])
    return courses


def total_credits(db: dict, student_id: str) -> int:
    """計算一位學生目前的總學分。

    參數：
        db：全部資料
        student_id：學號

    回傳：
        已選課程的學分總和

    例子（S001 選了兩門 3 學分的課）：
        total_credits(db, "S001") → 6

    對應需求：F2-04
    """
    total = 0
    for course in enrolled_courses(db, student_id):
        total += course.credit
    return total


def add_enrollment(db: dict, student_id: str, course_id: str) -> list[str]:
    """加選一門課；有任何錯誤時不加選。

    參數：
        db：全部資料
        student_id：學號
        course_id：課程代號

    回傳：
        錯誤清單，加選成功時是 []。
        學生或課程不存在時只回報這兩項：
            "找不到學生：{學號}"
            "找不到課程：{課程代號}"
        已選過時只回報："已選過這門課：{課程代號}"
        其他條件全部檢查完才回報，時段衝突在前、依星期和節次排序：
            和已選課程重疊 → "衝堂：{時段}，已選課程 {課程代號} {課程名稱}"
            同教室同時段已有別的課 → "教室衝堂：{時段}，{教室} 已有 {課程代號} {課程名稱}"
            加選後超過學分上限 → "學分超過上限：加選後 {學分} 學分，上限 {學分上限}"
            課程額滿 → "課程已額滿：{目前人數}/{人數上限}"
        {時段} 用 time_rules.slot_text 產生，例如 "星期二第 3、4 節"。

    例子（S001 已選 MA101 微積分，星期二第 3、4 節；CS102 也在星期二第 3、4 節且已額滿）：
        add_enrollment(db, "S001", "CS101") → []
        add_enrollment(db, "S001", "CS102") → ["衝堂：星期二第 3、4 節，已選課程 MA101 微積分", "課程已額滿：50/50"]

    對應需求：F2-01、F2-03、F2-04、F2-05、F2-06、F2-07
    """
    errors = []
    if student_id not in db["students"]:
        errors.append(f"找不到學生：{student_id}")
    if course_id not in db["courses"]:
        errors.append(f"找不到課程：{course_id}")
    if errors:
        return errors

    for enrollment in db["enrollments"]:
        if enrollment.student_id == student_id and enrollment.course_id == course_id:
            return [f"已選過這門課：{course_id}"]

    student = db["students"][student_id]
    course = db["courses"][course_id]

    # 時段衝突先存成 (星期, 第一個節次, 種類, 錯誤文字)，全部找完再排序
    # 種類 1 是學生衝堂、2 是教室衝堂，同一個時段時學生衝堂排前面
    time_errors = []
    for other in enrolled_courses(db, student_id):
        conflicts = time_rules.find_conflicts(course.schedule, other.schedule)
        for day, periods in conflicts.items():
            text = f"衝堂：{time_rules.slot_text(day, periods)}，已選課程 {other.course_id} {other.course_name}"
            time_errors.append((day, periods[0], 1, text))

    for other in db["courses"].values():
        if other.course_id == course_id or other.classroom != course.classroom:
            continue
        conflicts = time_rules.find_conflicts(course.schedule, other.schedule)
        for day, periods in conflicts.items():
            text = f"教室衝堂：{time_rules.slot_text(day, periods)}，{course.classroom} 已有 {other.course_id} {other.course_name}"
            time_errors.append((day, periods[0], 2, text))

    time_errors.sort()
    for day, first_period, kind, text in time_errors:
        errors.append(text)

    new_total = total_credits(db, student_id) + course.credit
    if new_total > student.credit_limit:
        errors.append(f"學分超過上限：加選後 {new_total} 學分，上限 {student.credit_limit}")

    enrolled = manage_courses.count_enrolled(db, course_id)
    if enrolled >= course.students_limit:
        errors.append(f"課程已額滿：{enrolled}/{course.students_limit}")

    if errors:
        return errors
    db["enrollments"].append(Enrollment(student_id, course_id))
    return []


def drop_enrollment(db: dict, student_id: str, course_id: str) -> list[str]:
    """退選一門課。

    參數：
        db：全部資料
        student_id：學號
        course_id：課程代號

    回傳：
        錯誤清單，退選成功時是 []。錯誤文字："沒有這筆選課紀錄：{學號} {課程代號}"

    例子（S001 選了 MA101）：
        drop_enrollment(db, "S001", "MA101") → []
        drop_enrollment(db, "S001", "CS999") → ["沒有這筆選課紀錄：S001 CS999"]

    對應需求：F2
    """
    for enrollment in db["enrollments"]:
        if enrollment.student_id == student_id and enrollment.course_id == course_id:
            db["enrollments"].remove(enrollment)
            return []
    return [f"沒有這筆選課紀錄：{student_id} {course_id}"]
