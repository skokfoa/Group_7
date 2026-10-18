"""
教室管理：教室的新增、修改、刪除和查詢。
新增、修改前用 data_checks 檢查；不 print、不讀寫檔案。
"""

from data_formats import Classroom
import data_checks
import save_load

def add_classroom(db: dict, classroom: Classroom) -> list[str]:
    """新增一間教室；有錯誤時不新增。

    參數：
        db：全部資料
        classroom：要新增的教室

    回傳：
        data_checks.check_classroom 的錯誤清單；沒有錯誤時新增成功，回傳 []

    例子：
        add_classroom(db, Classroom("EN201", 60, ["投影機"], "綜合科館")) → []
        再新增一次 EN201 → ["教室代號已存在：EN201"]

    對應需求：F1-01
    """
    Checked_Classroom = data_checks.check_classroom(db,classroom,is_new=True)
    if len(Checked_Classroom) == 0:
        New_Classroom = {
            "classrooms":{
                classroom.classroom_id:{
                            "capacity":classroom.capacity,
                            "equipment":classroom.equipment,
                            "building":classroom.building
                        }
            }
            
        }
        db["classrooms"]["classrooms"].update(New_Classroom["classrooms"])
        save_load.save_data(db,"data")
    return Checked_Classroom



def update_classroom(db: dict, classroom: Classroom) -> list[str]:
    """修改一間教室，用新資料取代同代號的舊資料；有錯誤時不修改。

    參數：
        db：全部資料
        classroom：修改後的教室

    回傳：
        data_checks.check_classroom 的錯誤清單；沒有錯誤時修改成功，回傳 []

    例子：
        update_classroom(db, Classroom("EN201", 80, ["投影機"], "綜合科館")) → []
        update_classroom(db, Classroom("EN999", 30, [], "綜合科館")) → ["找不到教室：EN999"]

    對應需求：F1-01
    """
    Checked_Classroom = data_checks.check_classroom(db,classroom,is_new=False)
    if len(Checked_Classroom) == 0:
        New_Classroom = {
            "classrooms":{
                classroom.classroom_id:{
                            "capacity":classroom.capacity,
                            "equipment":classroom.equipment,
                            "building":classroom.building
                        }
            }
            
        }
        db["classrooms"]["classrooms"].update(New_Classroom["classrooms"])
        save_load.save_data(db,"data")
    return Checked_Classroom



def delete_classroom(db: dict, classroom_id: str) -> list[str]:
    """刪除一間教室；還有課程使用時不刪除。

    參數：
        db：全部資料
        classroom_id：教室代號

    回傳：
        錯誤清單，刪除成功時是 []。錯誤文字：
            "找不到教室：{教室代號}"
            "{教室代號} 還有課程使用，不能刪除"

    例子（EN201 有課程使用、EN202 沒有）：
        delete_classroom(db, "EN202") → []
        delete_classroom(db, "EN201") → ["EN201 還有課程使用，不能刪除"]

    對應需求：F1-01
    """
    if classroom_id not in db["classrooms"]["classrooms"]:
        return [f"找不到教室：{classroom_id}"]
    Course_List = list(db["courses"]["courses"].keys())
    for course in Course_List:
        if classroom_id in db["courses"]["courses"][course]["classroom"]:
            return [f"{classroom_id} 還有課程使用，不能刪除"]
    del db["classrooms"]["classrooms"][classroom_id]
    save_load.save_data(db,"data")
    return []



def get_classroom(db: dict, classroom_id: str) -> Classroom | None:
    """用教室代號查一間教室。

    參數：
        db：全部資料
        classroom_id：教室代號

    回傳：
        找到時回傳 Classroom，找不到時回傳 None

    例子：
        get_classroom(db, "EN201") → Classroom("EN201", 60, ["投影機"], "綜合科館")
        get_classroom(db, "EN999") → None

    對應需求：F1-01
    """
    if classroom_id in db["classrooms"]["classrooms"]:
        return Classroom(classroom_id,
                         db["classrooms"]["classrooms"][classroom_id]["capacity"],
                         db["classrooms"]["classrooms"][classroom_id]["equipment"],
                         db["classrooms"]["classrooms"][classroom_id]["building"])
    else:
        return None

