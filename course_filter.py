"""
課程篩選：依學生的條件篩選候選課程，並檢查條件能不能滿足。
只讀 db、不修改；時段比對用 time_rules；不 print、不讀寫檔案。
"""

from data_formats import Course
import manage_courses
import time_rules


def filter_courses(
    db: dict,
    wanted: list[str],
    required: list[str],
    min_credits: int,
    max_credits: int,
    blocked: dict[str, list[int]],
    days: list[str],
) -> tuple[list[Course], list[str]]:
    """篩選候選課程，並列出條件無法滿足的原因。

    參數：
        db：全部資料
        wanted：希望修習的課程代號
        required：必修課程代號
        min_credits、max_credits：最低、最高學分
        blocked：不可上課時段，格式和 Course.schedule 相同；沒有時是 {}
        days：偏好上課星期，例如 ["1", "3"]；[] 代表不限

    回傳：
        (候選課程, 問題清單)
        候選課程：依課程代號排序。
            必修課程：還有名額、不在不可上課時段，就是候選課程。
            希望修習的課程：還有名額、不在不可上課時段、每個上課星期都在 days 裡，才是候選課程；不符合的直接排除，不列入問題。
        問題清單：沒有問題時是 []。依下列順序檢查：
            課程不存在（必修、希望修習都檢查）→ "找不到課程：{課程代號}"
            最低學分大於最高學分 → "最低學分大於最高學分：{最低} > {最高}"
            必修課程額滿 → "必修課程已額滿：{課程代號} {課程名稱}"
            必修課程在不可上課時段 → "必修課程在不可上課時段：{時段}，{課程代號} {課程名稱}"
            必修課程學分加起來超過最高學分 → "必修課程共 {學分} 學分，超過最高學分 {最高}"
            候選課程學分加起來未達最低學分 → "候選課程共 {學分} 學分，未達最低學分 {最低}"
        必修課程的額滿、時段兩項依 required 的順序，一門檢查完再換下一門。
        {時段} 用 time_rules.slot_text 產生。候選課程之間是否衝堂不在這裡檢查。

    例子（CS101 3 學分星期一第 1、2 節；MA101 3 學分星期二第 3、4 節；CS102 3 學分星期二第 3、4 節，已額滿）：
        filter_courses(db, ["CS102"], ["CS101", "MA101"], 3, 9, {}, []) → ([Course("CS101", ...), Course("MA101", ...)], [])
        filter_courses(db, [], ["CS101"], 9, 6, {"1": [1]}, []) → ([], ["最低學分大於最高學分：9 > 6", "必修課程在不可上課時段：星期一第 1 節，CS101 計算機概論", "候選課程共 0 學分，未達最低學分 9"])

    對應需求：F5
    """
    raise NotImplementedError
