"""存檔與載入：data/ 的 JSON 檔和 db 互相轉換，是唯一會讀寫檔案的地方。"""
import json
from pathlib import Path
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
    db = {}
    folder_path = Path(__file__).parent / data_dir  # 取得相對於當前 .py 檔的路徑

    # 若資料夾不存在，自動建立並回傳空字典
    if not folder_path.exists():
        folder_path.mkdir(parents=True, exist_ok=True)
        return db

    # 讀取資料夾下所有 .json 檔
    for file_path in folder_path.glob("*.json"):
        key_name = file_path.stem  # 取得檔名（不含 .json），例如 "student"
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                db[key_name] = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            db[key_name] = {key_name:{}}  # 檔案為空或毀損時預設為空字典
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
     # 定義專案需求的四個 JSON 檔名 Key (請依據專案實際採用的 4 個檔名調整)
    required_keys = ["students", "courses", "enrollments", "classrooms"]
    
    for Keys in required_keys:
        data_path = data_dir + '\\' + f"{Keys}.json"
        print(db)
        print(data_path)
        with open(data_path,'w',encoding="utf-8")as Write_File:
            json.dump(db[Keys],Write_File,indent=4,ensure_ascii=False)
