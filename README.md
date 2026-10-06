# Group 7 - 學生與課程管理模組 (Class_student_course.py)
## 檔案結構

* `Class_student_course.py`：包含 `Course` 與 `Student` 的類別實作與測試代碼。

## 類別規格說明

### 1. Course (課程類別)

| 屬性名稱 (Attribute) | 資料型態 (Type) | 說明 |
| :--- | :--- | :--- |
| `course_id` | `int` | 課程編號 |
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
| `student_id` | `int` | 學號 |
| `name` | `str` | 學生姓名 |
| `major` | `str` | 主修科系 |
| `selected_courses` | `list[Course]` | 已選課程物件清單 |
| `credit` | `int` | 已選課程總學分 |

---