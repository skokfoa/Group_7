"""
活動管理：活動時間換成時段、活動的新增、修改、取消和查詢，找合適的教室，以及學生報名活動。
新增、修改前用 data_checks 檢查；時段比對用 time_rules；不 print、不讀寫檔案。
"""

from data_formats import Activity, Classroom, Signup
import data_checks
import time_rules


def activity_schedule(date: str, start_time: str, end_time: str) -> dict[str, list[int]]:
    """把活動的日期和時間換成上課時段。

    參數：
        date：日期，例如 "2026-11-05"
        start_time、end_time：開始、結束時間，例如 "18:30"、"20:00"

    回傳：
        {星期: [節次]}，格式和 Course.schedule 相同，節次由小到大。
        第 1 節是 08:10～09:00，之後每節晚一小時，第 9 節是 16:10～17:00；
        第 10～12 節（a、b、c）是 17:10～18:00、18:10～19:00、19:10～20:00。
        活動和某一節有重疊就算佔用那一節，剛好接在前後不算；一節都沒佔用時是 {}。

    例子：
        activity_schedule("2026-11-05", "18:30", "20:00") → {"4": [11, 12]}
        activity_schedule("2026-11-02", "12:00", "13:00") → {"1": [5]}

    對應需求：F4-05
    """
    raise NotImplementedError


def add_activity(db: dict, activity: Activity) -> list[str]:
    """新增一項活動；有錯誤時不新增。

    參數：
        db：全部資料
        activity：要新增的活動

    回傳：
        錯誤清單，新增成功時是 []。
        先用 data_checks.check_activity 檢查，有錯誤就只回傳這些；
        沒有錯誤再用 classroom_problems 檢查 activity.classroom，回傳沒滿足的條件。

    例子（EN201 可坐 60 人、有投影機，2026-11-05 晚上沒有別的安排）：
        add_activity(db, Activity("A002", "程式設計讀書會", "2026-11-05", "18:30", "20:00", 20, "讀書會", ["投影機"], "EN201")) → []
        再新增一次同一項活動 → ["活動代號已存在：A002"]

    對應需求：F4-01、F4-06
    """
    raise NotImplementedError


def update_activity(db: dict, activity: Activity) -> list[str]:
    """修改一項活動，用新資料取代同代號的舊資料；有錯誤時不修改。

    參數：
        db：全部資料
        activity：修改後的活動

    回傳：
        錯誤清單，修改成功時是 []。檢查方式和 add_activity 相同，但 check_activity 的 is_new 是 False。

    例子：
        update_activity(db, Activity("A002", "程式設計讀書會", "2026-11-05", "18:30", "20:00", 30, "讀書會", ["投影機"], "EN201")) → []
        update_activity(db, Activity("A999", "期末說明會", "2026-12-20", "10:00", "12:00", 30, "講座", [], "EN201")) → ["找不到活動：A999"]

    對應需求：F4-01、F4-06
    """
    raise NotImplementedError


def cancel_activity(db: dict, activity_id: str) -> list[str]:
    """取消一項活動：刪除這項活動的所有報名紀錄，再刪除活動。

    參數：
        db：全部資料
        activity_id：活動代號

    回傳：
        錯誤清單，取消成功時是 []。錯誤文字："找不到活動：{活動代號}"

    例子：
        cancel_activity(db, "A002") → []
        cancel_activity(db, "A999") → ["找不到活動：A999"]

    對應需求：F4-01
    """
    raise NotImplementedError


def get_activity(db: dict, activity_id: str) -> Activity | None:
    """用活動代號查一項活動。

    參數：
        db：全部資料
        activity_id：活動代號

    回傳：
        找到時回傳 Activity，找不到時回傳 None

    例子：
        get_activity(db, "A002") → Activity("A002", "程式設計讀書會", ...)
        get_activity(db, "A999") → None

    對應需求：F4-01
    """
    raise NotImplementedError


def search_activities(
    db: dict,
    date: str | None = None,
    activity_type: str | None = None,
) -> list[Activity]:
    """依條件查詢活動；沒給的條件不篩選。

    參數：
        db：全部資料
        date：日期，例如 "2026-11-05"
        activity_type：活動類型，例如 "講座"

    回傳：
        符合所有條件的活動清單，依日期、開始時間排序

    例子：
        search_activities(db, date="2026-11-05") → 11/5 的所有活動
        search_activities(db, activity_type="講座") → 所有講座

    對應需求：F4-01
    """
    raise NotImplementedError


def classroom_problems(db: dict, activity: Activity, classroom_id: str) -> list[str]:
    """檢查一間教室能不能給這項活動用，回傳所有沒滿足的條件。

    參數：
        db：全部資料
        activity：活動，日期和時間要合法（activity.classroom 不用填）
        classroom_id：要檢查的教室代號，必須存在

    回傳：
        沒滿足的條件清單，教室可以用時是 []。全部檢查完才回報，依下列順序：
            容量至少是預計人數 → "容量不足：{教室} 可坐 {容量} 人，活動預計 {預計人數} 人"
            有活動需要的每一樣設備 → "缺少設備：{教室} 沒有 {缺的設備，用「、」隔開}"
            同時段沒有課程 → "教室衝堂：{時段}，{教室} 已有課程 {課程代號} {課程名稱}"
            同一天同時段沒有別的活動 → "教室衝堂：{時段}，{教室} 已有活動 {活動代號} {活動名稱}"
        活動時段用 activity_schedule 換算，用 time_rules.find_conflicts 比對：
        課程只比星期和節次；活動要同一天才比，而且不和代號相同的活動（修改前的自己）比。
        {時段} 是重疊的那幾節，用 time_rules.slot_text 產生；教室衝堂依節次排序。

    例子（EN201 可坐 60 人、沒有麥克風；星期四第 11、12 節是 CS205 資料結構，在 EN201）：
        classroom_problems(db, Activity("A002", "程式設計讀書會", "2026-11-05", "18:30", "20:00", 20, "讀書會", ["投影機"], ""), "EN202") → []
        classroom_problems(db, Activity("A002", "程式設計讀書會", "2026-11-05", "18:30", "20:00", 80, "讀書會", ["投影機", "麥克風"], ""), "EN201")
        → ["容量不足：EN201 可坐 60 人，活動預計 80 人", "缺少設備：EN201 沒有 麥克風", "教室衝堂：星期四第 b、c 節，EN201 已有課程 CS205 資料結構"]

    對應需求：F4-06
    """
    raise NotImplementedError


def find_classrooms(db: dict, activity: Activity) -> list[Classroom]:
    """找出所有能給這項活動用的教室。

    參數：
        db：全部資料
        activity：活動，日期和時間要合法（activity.classroom 不用填）

    回傳：
        classroom_problems 是 [] 的教室清單，依教室代號排序；沒有合適的教室時是 []，
        這時對每間教室呼叫 classroom_problems，就能顯示每間教室沒滿足的條件。

    例子（只有 EN202 容量夠、有投影機、那段時間沒人用）：
        find_classrooms(db, Activity("A002", "程式設計讀書會", "2026-11-05", "18:30", "20:00", 20, "讀書會", ["投影機"], "")) → [Classroom("EN202", ...)]
        預計 500 人的活動 → []

    對應需求：F4-07
    """
    raise NotImplementedError


def count_signups(db: dict, activity_id: str) -> int:
    """計算一項活動目前的報名人數。

    參數：
        db：全部資料
        activity_id：活動代號

    回傳：
        報名人數

    例子（A002 有 2 人報名）：
        count_signups(db, "A002") → 2

    對應需求：F4-08
    """
    raise NotImplementedError


def signed_up_activities(db: dict, student_id: str) -> list[Activity]:
    """列出一位學生報名的活動。

    參數：
        db：全部資料
        student_id：學號

    回傳：
        活動清單，依日期、開始時間排序；沒有報名時是 []

    例子（S001 報名了 A002）：
        signed_up_activities(db, "S001") → [Activity("A002", ...)]
        signed_up_activities(db, "S999") → []

    對應需求：F2-02、F3、F4-08
    """
    raise NotImplementedError


def sign_up(db: dict, student_id: str, activity_id: str) -> list[str]:
    """學生報名一項活動；有任何錯誤時不報名。

    參數：
        db：全部資料
        student_id：學號
        activity_id：活動代號

    回傳：
        錯誤清單，報名成功時是 []。
        學生或活動不存在時只回報這兩項：
            "找不到學生：{學號}"
            "找不到活動：{活動代號}"
        已報名過時只回報："已報名這項活動：{活動代號}"
        其他條件全部檢查完才回報，時段衝突在前、依節次排序：
            和已選課程重疊 → "衝堂：{時段}，已選課程 {課程代號} {課程名稱}"
            和同一天已報名的活動重疊 → "衝堂：{時段}，已報名活動 {活動代號} {活動名稱}"
            報名人數已達預計人數 → "活動已額滿：{報名人數}/{預計人數}"
        {時段} 是重疊的那幾節，用 time_rules.slot_text 產生，例如 "星期四第 b、c 節"。

    例子（A002 在 2026-11-05 18:30～20:00，已有 20 人報名、預計 20 人；S001 已選 CS205 資料結構，星期四第 11、12 節）：
        sign_up(db, "S001", "A003") → []
        sign_up(db, "S001", "A002") → ["衝堂：星期四第 b、c 節，已選課程 CS205 資料結構", "活動已額滿：20/20"]

    對應需求：F4-08
    """
    raise NotImplementedError
