"""
櫃檯：顯示選單、讀使用者輸入、呼叫各模組、印出結果；啟動時載入資料，修改成功後存檔。
輸入只盡量轉成數字，對錯一律交給 data_checks 判斷。
"""

from data_formats import Classroom, Course, Student
import enroll
import manage_classrooms
import manage_courses
import manage_students
import save_load
import time_rules
import timetable

DATA_DIR = "data"
NOT_DONE = "NOT_DONE"  # run() 遇到還沒寫好的函式時回傳這個


def to_int(text: str) -> int | str:
    """把輸入轉成整數，轉不了就原樣回傳。

    參數：
        text：使用者輸入

    回傳：
        整數，或原本的文字

    例子：
        to_int("3") → 3
        to_int("abc") → "abc"
    """
    try:
        return int(text)
    except ValueError:
        return text


def to_schedule(text: str) -> dict:
    """把上課時段輸入轉成 schedule；同一天寫兩次會合併，節次文字轉不了就原樣保留。

    參數：
        text：格式為「星期:節次,節次」，多天用空白隔開

    回傳：
        {星期: [節次]}

    例子：
        to_schedule("1:3,4 2:b") → {"1": [3, 4], "2": [11]}
        to_schedule("1:3 1:4") → {"1": [3, 4]}

    對應需求：F1-05
    """
    schedule = {}
    for part in text.split():
        day, _, periods = part.partition(":")
        if day not in schedule:
            schedule[day] = []
        for p in periods.split(","):
            number = time_rules.period_to_number(p)
            schedule[day].append(number if number is not None else p)
    return schedule


def run(func, *args):
    """呼叫一個模組函式；還沒寫好的函式只印提示，不讓程式中斷。

    參數：
        func：要呼叫的函式
        args：傳給函式的參數

    回傳：
        函式的回傳值；還沒寫好時回傳 NOT_DONE

    例子：
        run(manage_courses.get_course, db, "CS101") → Course 或 None
    """
    try:
        return func(*args)
    except NotImplementedError:
        print("這個功能還沒完成")
        return NOT_DONE


def report(db: dict, errors: list[str] | None) -> None:
    """印出修改結果；成功就存檔。

    參數：
        db：全部資料
        errors：修改函式回傳的錯誤清單，或 NOT_DONE

    回傳：
        無
    """
    if errors == NOT_DONE:
        return
    if errors:
        for e in errors:
            print("錯誤：" + e)
    else:
        save_load.save_data(db, DATA_DIR)
        print("完成，已存檔")


def show(found, missing: str) -> None:
    """印出查一筆的結果。

    參數：
        found：查詢函式的回傳值（物件、None 或 NOT_DONE）
        missing：找不到時要印的文字

    回傳：
        無
    """
    if found == NOT_DONE:
        return
    print(found if found is not None else missing)


def input_course(course_id: str) -> Course:
    """依序詢問課程欄位，組成 Course。"""
    return Course(
        course_id,
        input("課程名稱："),
        to_int(input("學分：")),
        input("必修請輸入 y，選修直接按 Enter：") == "y",
        input("授課教師："),
        to_int(input("人數上限：")),
        input("教室代號："),
        to_schedule(input("上課時段（例 1:3,4 2:b）：")),
    )


def input_student(student_id: str) -> Student:
    """依序詢問學生欄位，組成 Student。"""
    limit = input("學分上限（直接按 Enter 為 24）：")
    return Student(student_id, input("姓名："), input("系級："),
                   to_int(limit) if limit else 24)


def input_classroom(classroom_id: str) -> Classroom:
    """依序詢問教室欄位，組成 Classroom。"""
    return Classroom(
        classroom_id,
        to_int(input("容量：")),
        [e for e in input("設備（用逗號隔開）：").split(",") if e],
        input("大樓："),
    )


def course_menu(db: dict) -> None:
    """課程管理選單。對應需求：F1-01、F1-06、F1-09"""
    print("1 新增  2 修改  3 刪除  4 取消課程  5 查一門  6 條件查詢")
    choice = input("請選擇：")
    if choice in ("1", "2", "3", "4", "5"):
        course_id = input("課程代號：")
    if choice == "1":
        report(db, run(manage_courses.add_course, db, input_course(course_id)))
    elif choice == "2":
        report(db, run(manage_courses.update_course, db, input_course(course_id)))
    elif choice == "3":
        report(db, run(manage_courses.delete_course, db, course_id))
    elif choice == "4":
        report(db, run(manage_courses.cancel_course, db, course_id))
    elif choice == "5":
        show(run(manage_courses.get_course, db, course_id), "找不到課程")
    elif choice == "6":
        print("不篩選的條件直接按 Enter")
        instructor = input("授課教師：") or None
        day = input("星期 1～7：") or None
        required = {"y": True, "n": False}.get(input("必修 y／選修 n："))
        seats = {"y": True, "n": False}.get(input("有名額 y／額滿 n："))
        result = run(manage_courses.search_courses, db, None, instructor, day, required, seats)
        if result != NOT_DONE:
            for course in result:
                print(course)


def student_menu(db: dict) -> None:
    """學生管理選單。對應需求：F1-01、F1-07"""
    print("1 新增  2 修改  3 刪除  4 查一位")
    choice = input("請選擇：")
    if choice not in ("1", "2", "3", "4"):
        return
    student_id = input("學號：")
    if choice == "1":
        report(db, run(manage_students.add_student, db, input_student(student_id)))
    elif choice == "2":
        report(db, run(manage_students.update_student, db, input_student(student_id)))
    elif choice == "3":
        report(db, run(manage_students.delete_student, db, student_id))
    elif choice == "4":
        show(run(manage_students.get_student, db, student_id), "找不到學生")


def classroom_menu(db: dict) -> None:
    """教室管理選單。對應需求：F1-01"""
    print("1 新增  2 修改  3 刪除  4 查一間")
    choice = input("請選擇：")
    if choice not in ("1", "2", "3", "4"):
        return
    classroom_id = input("教室代號：")
    if choice == "1":
        report(db, run(manage_classrooms.add_classroom, db, input_classroom(classroom_id)))
    elif choice == "2":
        report(db, run(manage_classrooms.update_classroom, db, input_classroom(classroom_id)))
    elif choice == "3":
        report(db, run(manage_classrooms.delete_classroom, db, classroom_id))
    elif choice == "4":
        show(run(manage_classrooms.get_classroom, db, classroom_id), "找不到教室")


def enrollment_menu(db: dict) -> None:
    """選課選單。對應需求：F2"""
    print("1 加選  2 退選  3 查已選課程")
    choice = input("請選擇：")
    if choice not in ("1", "2", "3"):
        return
    student_id = input("學號：")
    if choice == "1":
        add_and_report(db, student_id, input("課程代號："))
    elif choice == "2":
        report(db, run(enroll.drop_enrollment, db, student_id, input("課程代號：")))
    elif choice == "3":
        courses = run(enroll.enrolled_courses, db, student_id)
        if courses == NOT_DONE:
            return
        for course in courses:
            print(f"{course.course_id} {course.course_name} {course.credit} 學分")
        print(f"共 {len(courses)} 門課")


def add_and_report(db: dict, student_id: str, course_id: str) -> None:
    """加選一門課，照作業 F2 的範例格式印出結果；成功就存檔。

    參數：
        db：全部資料
        student_id：學號
        course_id：課程代號

    回傳：
        無
    """
    before = run(enroll.total_credits, db, student_id)
    taken = run(enroll.enrolled_courses, db, student_id)
    errors = run(enroll.add_enrollment, db, student_id, course_id)
    if NOT_DONE in (before, taken, errors):
        return
    student = manage_students.get_student(db, student_id)
    course = manage_courses.get_course(db, course_id)

    print(f"學生：{student_id}")
    print(f"欲加選：{course_id} {course.course_name if course else ''}")
    if errors:
        print("選課結果：失敗")
        for i, e in enumerate(errors, start=1):
            print(f"衝突 {i}：{e}")
    else:
        save_load.save_data(db, DATA_DIR)
        print("選課結果：成功，已存檔")
    if student and course and course not in taken:
        print(f"目前學分：{before}")
        print(f"加選後學分：{before + course.credit}")
        print(f"學分上限：{student.credit_limit}")


def print_timetable(table: list[list[str]]) -> None:
    """印出 7 × 12 的課表，一列是一個節次。

    參數：
        table：timetable.build_timetable 的課表

    回傳：
        無
    """
    print("節次  " + "".join(f"  {time_rules.day_to_text(str(d))[-1]}   " for d in range(1, 8)))
    for p in range(1, 13):
        cells = ""
        for d in range(1, 8):
            cells += f"{table[d - 1][p - 1] or '-':^7}"
        print(f"{time_rules.period_to_text(p):^4}  {cells}")


def timetable_menu(db: dict) -> None:
    """個人課表選單。對應需求：F3"""
    student_id = input("學號：")
    courses = run(enroll.enrolled_courses, db, student_id)
    if courses == NOT_DONE:
        return
    table = run(timetable.build_timetable, courses)
    if table == NOT_DONE:
        return
    print("1 看課表  2 查詢  3 找連續空堂  4 統計")
    choice = input("請選擇：")
    if choice == "1":
        print_timetable(table)
    elif choice == "2":
        print("不篩選的條件直接按 Enter")
        day = input("星期 1～7：") or None
        period = time_rules.period_to_number(input("節次 1～9、a～c："))
        course_id = input("課程代號：") or None
        result = run(timetable.search_timetable, table, day, period, course_id)
        if result != NOT_DONE:
            for d, p, cid in result:
                print(f"{time_rules.slot_text(d, [p])}：{cid}")
    elif choice == "3":
        days = input("星期，用空白隔開（例 1 2 3）：").split()
        first = time_rules.period_to_number(input("從第幾節："))
        last = time_rules.period_to_number(input("到第幾節："))
        length = to_int(input("至少連續幾節："))
        if first is None or last is None or not isinstance(length, int):
            print("錯誤：節次或節數不合法")
            return
        if not all(time_rules.is_valid_day(d) for d in days):
            print("錯誤：星期不合法")
            return
        result = run(timetable.find_free_slots, table, days, first, last, length)
        if result != NOT_DONE:
            for d, start, end in result:
                print(f"{time_rules.day_to_text(d)}第 {time_rules.period_to_text(start)}～{time_rules.period_to_text(end)} 節")
            if not result:
                print("沒有符合的空堂")
    elif choice == "4":
        stats = run(timetable.timetable_stats, courses)
        if stats != NOT_DONE:
            for d in range(1, 8):
                print(f"{time_rules.day_to_text(str(d))}：{stats['daily'][str(d)]} 節")
            print(f"每週總學分：{stats['credits']}")
            print(f"空堂數：{stats['gaps']}")


def main() -> None:
    """載入資料後顯示主選單，直到使用者選擇離開。"""
    db = save_load.load_data(DATA_DIR)
    menus = {"1": course_menu, "2": student_menu, "3": classroom_menu,
             "4": enrollment_menu, "5": timetable_menu}
    while True:
        print("\n1 課程管理  2 學生管理  3 教室管理  4 選課  5 個人課表  0 離開")
        choice = input("請選擇：")
        if choice == "0":
            break
        if choice in menus:
            menus[choice](db)


if __name__ == "__main__":
    main()
