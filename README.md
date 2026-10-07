# Group 7 - 學生與課程管理模組 (Class_student_course.py)
## 檔案結構

* `Class_student_course.py`：包含 `Course` 與 `Student` 的類別實作與測試代碼。

## 類別規格說明

### 1. Course (課程類別)

| 屬性名稱 (Attribute) | 資料型態 (Type) | 說明 |
| :--- | :--- | :--- |
| `course_id` | `str` | 課程編號 |
| `course_name` | `str` | 課程名稱 |
| `credit` | `int` | 課程學分 |
| `is_required` | `bool` | 是否為必修課 (`True`/`False`) |
| `instructor` | `str` | 指導教授 |
| `students_limit` | `int` | 學生人數上限 |
| `classroom` | `str` | 上課教室 |
| `schedule` | `dict[str, list[int]]` | 上課時間表（星期對應節次） |

> **排課時段說明**：
> `schedule` 鍵為星期（如 `"Monday"`），值為節次陣列。字母節次請轉為對應數字（例：A 節 = 10、B 節 = 11、C 節 = 12，以此類推）。

---

### 2. Student (學生類別)

儲存學生基本資料及已選修的課程清單。

| 屬性名稱 (Attribute) | 資料型態 (Type) | 說明 |
| :--- | :--- | :--- |
| `student_id` | `str` | 學號 |
| `name` | `str` | 學生姓名 |
| `major` | `str` | 主修科系 |
| `selected_courses` | `list[Course]` | 已選課程物件清單 |
| `credit` | `int` | 已選課程總學分 |
# Group 7 - F1功能模組_demo(F1.py)
## 檔案結構
```text
.
├── F1.py          # 主功能模組程式碼
├── student.json   # 學生資料儲存檔
└── course.json    # 課程資料儲存檔
```
## 函式功能說明
### 1. `InputStudent(`Is_Change`)`
* **功能描述**：互動式引導使用者輸入學號、姓名、主修、選修課程與學分，並建立並回傳一個 `Student` 物件。
* **參數**：
  | 屬性名稱 (Attribute) | 資料型態 (Type) | 說明 |
  | :--- | :--- | :--- |
  | `Is_Change` | `bool` | 是否為修改模式 |
* **回傳值**：
  * (`Student`) - 建立完成的學生物件。
### 2. `InputCourse(`Is_Change`)`
* **功能描述**：互動式引導使用者輸入課程編號、課程名稱、課程學分、是否為必修課、指導教授、學生人數上限、上課教室、上課時間表（星期對應節次），並建立並回傳一個 `Course` 物件。
* **參數**：
  | 屬性名稱 (Attribute) | 資料型態 (Type) | 說明 |
  | :--- | :--- | :--- |
  | `Is_Change` | `bool` | 是否為修改模式 |
* **回傳值**：
  * (`Course`) - 建立完成的課程物件。
    
### 學生管理模組
* **`CreateStudent()`**：引導使用者輸入學號、姓名、主修與學分，建立新學生並寫入 `student.json`。
* **`DeleteStudent()`**：輸入學生 ID，從 `student.json` 中移除該學生資料。
* **`ChangeStudent()`**：更新現有學生的資料內容。
* **`SearchStudent()`**：輸入學生 ID，查詢並印出學生的資料與選修課程清單。

### 課程管理模組
* **`CreateCourse()`**：引導使用者輸入各項課程參數，建立新課程並寫入 `course.json`[cite: 4]。
* **`DeleteCourse()`**：輸入課程 ID，從 `course.json` 中刪除指定的課程。
* **`ChangeCourse()`**：更新現有課程的相關屬性。
* **`SearchCourse()`**：輸入課程 ID，查詢並輸出課程資料與上課時間表。
---
