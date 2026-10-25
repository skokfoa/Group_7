# 選課與校園活動規劃系統（Group 7）

計算機程式設計團體作業，Python 命令列程式。

## 執行方式

需要 Python 3.10 以上；測試用 pytest（`pip install pytest`）。在專案最上層資料夾執行：

```
python main.py                              # 執行程式（main.py 整合中）
python -m pytest                            # 執行全部測試
python -m pytest tests/test_time_rules.py   # 只測一個模組
```

## 檔案地圖

| 檔案 | 做什麼 | 對應需求 |
|---|---|---|
| `main.py` | 選單、輸入輸出；啟動時載入資料，修改後存檔 | — |
| `data_formats.py` | 課程、學生、教室、選課紀錄、活動、活動報名紀錄的欄位，以及空的 db | 資料格式 |
| `data_checks.py` | 檢查資料是否符合規則，一次回報所有錯誤 | F1-02～F1-05、F4-02～F4-04 |
| `time_rules.py` | 節次轉換、星期和節次是否合法、時段是否重疊 | F1-05、F2-01、F2-03 |
| `manage_courses.py` | 課程的新增、修改、刪除、取消、查詢 | F1-01、F1-06、F1-09 |
| `manage_students.py` | 學生的新增、修改、刪除、查詢 | F1-01、F1-07 |
| `manage_classrooms.py` | 教室的新增、修改、刪除、查詢 | F1-01 |
| `enroll.py` | 加選、退選，學生已選的課程和學分 | F2 |
| `timetable.py` | 個人課表、查詢、連續空堂、統計 | F3 |
| `manage_activities.py` | 活動時間換成時段，活動的新增、修改、取消、查詢，找教室，學生報名 | F4 |
| `save_load.py` | `data/` 的 JSON 檔和 db 互相轉換 | F6 |
| `data/` | 資料檔 | — |
| `tests/` | 自動化測試，檔名 `test_模組名稱.py` | — |

## db 結構

`main.py` 啟動時把資料載入成 `db`，再當參數傳給各函式。

```python
db = {
    "courses":     {"CS102": Course(...)},
    "students":    {"S001": Student(...)},
    "classrooms":  {"EN201": Classroom(...)},
    "enrollments": [Enrollment("S001", "CS102")],
    "activities":  {"A001": Activity(...)},
    "signups":     [Signup("S001", "A001")],
}
```

- 學生已選的課程、課程目前人數，都從 `enrollments` 計算；學生報名的活動、活動報名人數，都從 `signups` 計算。
- `data/` 的 JSON 檔名和最外層鍵名都和 db 的 key 相同，例如 `courses.json` 是 `{"courses": {"CS102": {...}}}`。

## 回傳慣例

- 會修改 db 的函式回傳錯誤清單，`[]` 代表成功；有錯誤時 db 不變。
- 查詢一筆回傳該物件，找不到回傳 `None`；查詢多筆回傳清單。
- 錯誤訊息是一句中文並帶上出錯的值，例如 `"學分必須為正整數：0"`，文字照各函式的 docstring。
