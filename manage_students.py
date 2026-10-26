"""
學生管理：學生的新增、修改、刪除和查詢。
新增、修改前用 data_checks 檢查；不 print、不讀寫檔案。
"""

from data_formats import Student
import data_checks
# 改：拿掉 import save_load，以及 add_student、delete_student 裡的 save_load.save_data(db,"data")。
# 存檔由 main.py 負責，manage 只改 db；不然跑 pytest 會把測試用的資料寫進 data/。

def add_student(db: dict, student: Student) -> list[str]:
    """新增一位學生；有錯誤時不新增。

    參數：
        db：全部資料
        student：要新增的學生

    回傳：
        data_checks.check_student 的錯誤清單；沒有錯誤時新增成功，回傳 []

    例子：
        add_student(db, Student("S001", "王小明", "資工一")) → []
        再新增一次 S001 → ["學號已存在：S001"]

    對應需求：F1-01
    """

    Checked_Students = data_checks.check_student(db,student,True)
    if len(Checked_Students) == 0:
        db["students"][student.student_id] = student
    return Checked_Students


def update_student(db: dict, student: Student) -> list[str]:
    """修改一位學生，用新資料取代同學號的舊資料；有錯誤時不修改。

    參數：
        db：全部資料
        student：修改後的學生

    回傳：
        data_checks.check_student 的錯誤清單；沒有錯誤時修改成功，回傳 []

    例子：
        update_student(db, Student("S001", "王小明", "資工二")) → []
        update_student(db, Student("S999", "李小華", "資工一")) → ["找不到學生：S999"]

    對應需求：F1-01
    """
    Checked_Students = data_checks.check_student(db,student,False)
    if len(Checked_Students) == 0:
            db["students"][student.student_id] = student
            
    return Checked_Students

def delete_student(db: dict, student_id: str) -> list[str]:
    """刪除一位學生和他的所有選課紀錄。

    參數：
        db：全部資料
        student_id：學號

    回傳：
        錯誤清單，刪除成功時是 []。錯誤文字："找不到學生：{學號}"

    例子：
        delete_student(db, "S001") → []
        delete_student(db, "S999") → ["找不到學生：S999"]

    對應需求：F1-01、F1-07
    """
    if student_id not in db["students"]:
        return [f"找不到學生：{student_id}"]
    else:
        del db["students"][student_id]
        # 改：加上 .copy()。原本 temp 和 db["enrollments"] 是同一個清單，邊跑邊刪會讓編號超出範圍
        temp = db["enrollments"].copy()
        for students in range(len(db["enrollments"])):
            if student_id in db["enrollments"][students].student_id:
                temp.remove(db["enrollments"][students])
        # 改：這行移到迴圈外面，全部跑完再放回去
        db["enrollments"] = temp  
        return []


def get_student(db: dict, student_id: str) -> Student | None:
    """用學號查一位學生。

    參數：
        db：全部資料
        student_id：學號

    回傳：
        找到時回傳 Student，找不到時回傳 None

    例子：
        get_student(db, "S001") → Student("S001", "王小明", "資工一", 24)
        get_student(db, "S999") → None

    對應需求：F1-01
    """
    if student_id not in db["students"]:
        return None
    else:
        try:
            student = Student(student_id,
                                name=db["students"][student_id].name,
                                major=db["students"][student_id].major,
                                credit_limit=db["students"][student_id].credit_limit)
        except:
            student = Student(student_id,
                            name=db["students"][student_id]["name"],
                            major=db["students"][student_id]["major"],
                            credit_limit=db["students"][student_id]["credit_limit"])   
        return student


