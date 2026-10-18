"""資料檢查：檢查課程、學生、教室資料是否符合規則，一次回報所有錯誤。
只檢查、不修改資料；星期和節次的規則呼叫 time_rules。
"""

from data_formats import Classroom, Course, Student
import time_rules


def check_course(db: dict, course: Course, is_new: bool) -> list[str]:
    """檢查一門課程，回傳所有錯誤。

    參數：
        db：全部資料
        course：要檢查的課程
        is_new：True 是新增，False 是修改

    回傳：
        錯誤清單，沒有錯誤時是 []。依下列順序檢查：
            課程代號是 2 個英文字母加 3 位數字 → "課程代號格式錯誤：{課程代號}"
            新增時課程代號不能已存在 → "課程代號已存在：{課程代號}"
            修改時課程代號必須存在 → "找不到課程：{課程代號}"
            學分是正整數 → "學分必須為正整數：{學分}"
            人數上限至少為 1 → "人數上限必須至少為 1：{人數上限}"
            教室必須存在 → "找不到教室：{教室}"
            星期是 "1"～"7" → "星期不合法：{星期}"
            節次是 1～12 → "節次不合法：{節次}"
            至少一個時段 → "至少要有一個上課時段"

    例子（db 裡已有教室 EN201、課程 CS102）：
        check_course(db, Course("CS101", "計算機概論", 3, True, "李老師", 60, "EN201", {"1": [1, 2]}), True) → []
        check_course(db, Course("CS102", "演算法", "abc", True, "王老師", 50, "EN201", {"2": [13]}), True) → ["課程代號已存在：CS102", "學分必須為正整數：abc", "節次不合法：13"]

    對應需求：F1-02、F1-03、F1-04、F1-05、資料格式
    """
    errors = []

    ok = True
    if len(course.course_id) != 5:
        ok = False
    else:
        for c in course.course_id[0:2]:
            if c < "A" or c > "Z":
                ok = False
        for c in course.course_id[2:5]:
            if c < "0" or c > "9":
                ok = False
    if not ok:
        errors.append(f"課程代號格式錯誤：{course.course_id}")

    if is_new:
        if course.course_id in db["courses"]:
            errors.append(f"課程代號已存在：{course.course_id}")
    else:
        if course.course_id not in db["courses"]:
            errors.append(f"找不到課程：{course.course_id}")

    if type(course.credit) != int or course.credit <= 0:
        errors.append(f"學分必須為正整數：{course.credit}")

    if type(course.students_limit) != int or course.students_limit < 1:
        errors.append(f"人數上限必須至少為 1：{course.students_limit}")

    if course.classroom not in db["classrooms"]:
        errors.append(f"找不到教室：{course.classroom}")
 
    for day in course.schedule:
        if type(day) != str or not time_rules.is_valid_day(day):
            errors.append(f"星期不合法：{day}")
 
    for day in course.schedule:
        for period in course.schedule[day]:
            if type(period) != int or not time_rules.is_valid_period(period):
                errors.append(f"節次不合法：{period}")
 
    has_time = False
    for day in course.schedule:
        if len(course.schedule[day]) > 0:
            has_time = True
    if not has_time:
        errors.append("至少要有一個上課時段")
 
    return errors


def check_student(db: dict, student: Student, is_new: bool) -> list[str]:
    """檢查一位學生，回傳所有錯誤。

    參數：
        db：全部資料
        student：要檢查的學生
        is_new：True 是新增，False 是修改

    回傳：
        錯誤清單，沒有錯誤時是 []。依下列順序檢查：
            學號是 S 加 3 位數字 → "學號格式錯誤：{學號}"
            新增時學號不能已存在 → "學號已存在：{學號}"
            修改時學號必須存在 → "找不到學生：{學號}"

    例子：
        check_student(db, Student("S001", "王小明", "資工一"), True) → []
        check_student(db, Student("S01", "王小明", "資工一"), True) → ["學號格式錯誤：S01"]

    對應需求：F1-02、F1-03
    """
    errors = []
 
    ok = True
    if len(student.student_id) != 4 or student.student_id[0] != "S":
        ok = False
    else:
        for c in student.student_id[1:4]:
            if c < "0" or c > "9":
                ok = False
    if not ok:
        errors.append(f"學號格式錯誤：{student.student_id}")
 
    if is_new:
        if student.student_id in db["students"]:
            errors.append(f"學號已存在：{student.student_id}")
    else:
        if student.student_id not in db["students"]:
            errors.append(f"找不到學生：{student.student_id}")
 
    return errors


def check_classroom(db: dict, classroom: Classroom, is_new: bool) -> list[str]:
    """檢查一間教室，回傳所有錯誤。

    參數：
        db：全部資料
        classroom：要檢查的教室
        is_new：True 是新增，False 是修改

    回傳：
        錯誤清單，沒有錯誤時是 []。依下列順序檢查：
            教室代號是 2 個英文字母加 3 位數字 → "教室代號格式錯誤：{教室代號}"
            新增時教室代號不能已存在 → "教室代號已存在：{教室代號}"
            修改時教室代號必須存在 → "找不到教室：{教室代號}"
            容量至少為 1 → "容量必須至少為 1：{容量}"

    例子（db 裡已有教室 EN201）：
        check_classroom(db, Classroom("EN202", 40, ["投影機"], "綜合科館"), True) → []
        check_classroom(db, Classroom("EN201", 0, [], "綜合科館"), True) → ["教室代號已存在：EN201", "容量必須至少為 1：0"]

    對應需求：F1-02、F1-03、資料格式
    """
    errors = []
 
    ok = True
    if len(classroom.classroom_id) != 5:
        ok = False
    else:
        for c in classroom.classroom_id[0:2]:
            if c < "A" or c > "Z":
                ok = False
        for c in classroom.classroom_id[2:5]:
            if c < "0" or c > "9":
                ok = False
    if not ok:
        errors.append(f"教室代號格式錯誤：{classroom.classroom_id}")
 
    if is_new:
        if classroom.classroom_id in db["classrooms"]:
            errors.append(f"教室代號已存在：{classroom.classroom_id}")
    else:
        if classroom.classroom_id not in db["classrooms"]:
            errors.append(f"找不到教室：{classroom.classroom_id}")
 
    if type(classroom.capacity) != int or classroom.capacity < 1:
        errors.append(f"容量必須至少為 1：{classroom.capacity}")
 
    return errors
