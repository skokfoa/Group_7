"""
課程管理：課程的新增、修改、刪除、取消和查詢。
新增、修改前用 data_checks 檢查；不 print、不讀寫檔案。
"""

from data_formats import Course
import save_load
import data_checks


def add_course(db: dict, course: Course) -> list[str]:
    """新增一門課程；有錯誤時不新增。

    參數：
        db：全部資料
        course：要新增的課程

    回傳：
        data_checks.check_course 的錯誤清單；沒有錯誤時新增成功，回傳 []

    例子：
        add_course(db, Course("CS101", "計算機概論", 3, True, "李老師", 60, "EN201", {"1": [1, 2]})) → []
        再新增一次同一門課 → ["課程代號已存在：CS101"]

    對應需求：F1-01
    """
    Checked_Course = data_checks.check_course(db,course,True)
    if len(Checked_Course) == 0:
            db["courses"][course.course_id] = course
            save_load.save_data(db,"data")
    return  Checked_Course

def update_course(db: dict, course: Course) -> list[str]:
    """修改一門課程，用新資料取代同代號的舊資料；有錯誤時不修改。

    參數：
        db：全部資料
        course：修改後的課程

    回傳：
        data_checks.check_course 的錯誤清單；沒有錯誤時修改成功，回傳 []

    例子：
        update_course(db, Course("CS101", "計算機概論", 4, True, "李老師", 60, "EN201", {"1": [1, 2]})) → []
        update_course(db, Course("CS999", "演算法", 3, True, "王老師", 50, "EN201", {"2": [3]})) → ["找不到課程：CS999"]

    對應需求：F1-01
    """
    Checked_Course = data_checks.check_course(db,course,False)
    if len(Checked_Course) == 0:
        db["courses"][course.course_id] = course
        save_load.save_data(db,"data")
    return  Checked_Course

def count_enrolled(db: dict, course_id: str) -> int:
    """計算一門課程目前的選課人數。

    參數：
        db：全部資料
        course_id：課程代號

    回傳：
        選課人數

    例子（CS102 有 2 人選）：
        count_enrolled(db, "CS102") → 2

    對應需求：F1-09
    """
    Chose_Students = 0
    for students in range(len(db["enrollments"])) :
        if course_id in db["enrollments"][students].course_id:
            Chose_Students += 1
    return Chose_Students

def delete_course(db: dict, course_id: str) -> list[str]:
    """刪除一門課程；已有學生選修時不刪除。

    參數：
        db：全部資料
        course_id：課程代號

    回傳：
        錯誤清單，刪除成功時是 []。錯誤文字：
            "找不到課程：{課程代號}"
            "{課程代號} 已有學生選修，請改用取消課程"

    例子（CS101 沒人選、CS102 有人選）：
        delete_course(db, "CS101") → []
        delete_course(db, "CS102") → ["CS102 已有學生選修，請改用取消課程"]

    對應需求：F1-01、F1-06
    """
    if course_id not in db["courses"]:
        return [f"找不到課程：{course_id}"]
    if count_enrolled(db,course_id) == 0:
        del db["courses"][course_id]
        save_load.save_data(db,"data")
        return []
    else:
        return [f"{course_id} 已有學生選修，請改用取消課程"]



def cancel_course(db: dict, course_id: str) -> list[str]:
    """取消一門課程：刪除這門課的所有選課紀錄，再刪除課程。

    參數：
        db：全部資料
        course_id：課程代號

    回傳：
        錯誤清單，取消成功時是 []。錯誤文字："找不到課程：{課程代號}"

    例子：
        cancel_course(db, "CS102") → []
        cancel_course(db, "CS999") → ["找不到課程：CS999"]

    對應需求：F1-06
    """
    if course_id not in db["courses"]:
        return [f"找不到課程：{course_id}"]
    for students in range(len(db["enrollments"])) :
        if course_id in db["enrollments"][students].course_id:
            db["enrollments"][students].course_id.remove(course_id)
        
    save_load.save_data(db,"data")
    return[]
    





def get_course(db: dict, course_id: str) -> Course | None:
    """用課程代號查一門課程。

    參數：
        db：全部資料
        course_id：課程代號

    回傳：
        找到時回傳 Course，找不到時回傳 None

    例子：
        get_course(db, "CS101") → Course("CS101", "計算機概論", ...)
        get_course(db, "CS999") → None

    對應需求：F1-01
    """
    if course_id not in db["courses"]:
        return None
    try:
        Course_data = Course(course_id,
                        db["courses"][course_id].course_name,
                        db["courses"][course_id].credit,
                        db["courses"][course_id].is_required,
                        db["courses"][course_id].instructor,
                        db["courses"][course_id].students_limit,
                        db["courses"][course_id].classroom,
                        db["courses"][course_id].schedule
                        )
    except:
        Course_data = Course(course_id,
                            db["courses"][course_id]["course_name"],
                            db["courses"][course_id]["credit"],
                            db["courses"][course_id]["is_required"],
                            db["courses"][course_id]["instructor"],
                            db["courses"][course_id]["students_limit"],
                            db["courses"][course_id]["classroom"],
                            db["courses"][course_id]["schedule"]
                            )
    return Course_data





def search_courses(
    db: dict,
    course_id: str | None = None,
    instructor: str | None = None,
    day: str | None = None,
    is_required: bool | None = None,
    has_seats: bool | None = None,
) -> list[Course]:
    """依條件查詢課程；沒給的條件不篩選。

    參數：
        db：全部資料
        course_id：課程代號
        instructor：授課教師
        day：星期 "1"～"7"，找這天有上課的課程
        is_required：True 只找必修，False 只找選修
        has_seats：True 只找還有名額的課程，False 只找額滿的課程

    回傳：
        符合所有條件的課程清單，依課程代號排序

    例子：
        search_courses(db, instructor="王老師") → 王老師的所有課程
        search_courses(db, day="2", has_seats=True) → 星期二有課、還有名額的課程

    對應需求：F1-09
    """
    Compare_List = ["course_id","instructor",day,"is_required",has_seats]
    Condition_List = [course_id,instructor,day,is_required,has_seats]
    Course_List = list(db["courses"].keys())
    Real_Course_List = list(db["courses"].keys())
    for Condition in Condition_List:
        
        if Condition != None:
            for course in Course_List:
                if Condition == day:
                    if Condition not in db["courses"][course]["schedule"]:
                        try:
                            Real_Course_List.remove(course)
                        except:
                            ...
                elif Condition == has_seats:
                    if Condition:
                        if count_enrolled(db,course) >= db["courses"][course]["students_limit"]:
                            try:
                                Real_Course_List.remove(course)
                            except:
                                ...
                    else:    
                        if count_enrolled(db,course) < db["courses"][course]["students_limit"]:
                            try:
                                Real_Course_List.remove(course)
                            except:
                                ...                        
                elif Condition == course_id:
                    Real_Course_List = [course_id]
                elif Condition == is_required :
                    if Condition !=db["courses"][course][Compare_List[Condition_List.index(Condition)]]:
                        try:
                            Real_Course_List.remove(course)
                        except:
                            ...
                else:
                    if Condition not in db["courses"][course][Compare_List[Condition_List.index(Condition)]]:
                        try:
                            Real_Course_List.remove(course)
                        except:
                            ...
    return []    
    
