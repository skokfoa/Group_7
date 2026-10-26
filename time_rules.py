"""
時間規則：節次轉換、星期和節次是否合法、時段是否重疊。
全系統共用，之後其他功能或是函數都呼叫這裡。
"""


def period_to_number(text: str) -> int | None:
    """把節次文字轉成數字。

    參數：
        text：節次文字，"1"～"9" 或 "a"、"b"、"c"

    回傳：
        1～12；不合法時回傳 None

    例子：
        period_to_number("b") → 11
        period_to_number("x") → None

    對應需求：F1-05
    """
    if len(text) != 1:
        return None

    if text in "123456789":
        return int(text)
    elif text.upper() in "ABC":
        return ord(text.upper()) - ord('A') + 10
    else:
        return None


def period_to_text(number: int) -> str:
    """把節次數字轉回文字。

    參數：
        number：節次數字 1～12

    回傳：
        "1"～"9" 或 "a"、"b"、"c"

    例子：
        period_to_text(3) → "3"
        period_to_text(11) → "b"

    對應需求：F1-05
    """
    if number <= 9:
        return str(number)
    else:
        return "abc"[number - 10]


def is_valid_day(day: str) -> bool:
    """檢查星期是否合法。

    參數：
        day：星期

    回傳：
        "1"～"7" 回傳 True，其他回傳 False

    例子：
        is_valid_day("1") → True
        is_valid_day("8") → False

    對應需求：F1-05
    """
    return True if len(day) == 1 and day in "1234567" else False


def is_valid_period(period: int) -> bool:
    """檢查節次是否合法。

    參數：
        period：節次數字

    回傳：
        1～12 回傳 True，其他回傳 False

    例子：
        is_valid_period(12) → True
        is_valid_period(13) → False

    對應需求：F1-05
    """
    return True if 1 <= period <= 12 else False


def day_to_text(day: str) -> str:
    """把星期轉成中文。

    參數：
        day：星期 "1"～"7"

    回傳：
        "星期一"～"星期日"

    例子：
        day_to_text("2") → "星期二"
        day_to_text("7") → "星期日"

    對應需求：F2-06
    """
    raise NotImplementedError


def slot_text(day: str, periods: list[int]) -> str:
    """把同一天的幾個節次寫成一段文字。

    參數：
        day：星期 "1"～"7"
        periods：節次數字，由小到大

    回傳：
        例如 "星期二第 3、4 節"；節次 10～12 寫成 a、b、c

    例子：
        slot_text("2", [3, 4]) → "星期二第 3、4 節"
        slot_text("5", [11]) → "星期五第 b 節"

    對應需求：F2-06
    """
    raise NotImplementedError


def find_conflicts(schedule_a: dict[str, list[int]], schedule_b: dict[str, list[int]]) -> dict[str, list[int]]:
    """找出兩個上課時段重疊的地方。

    參數：
        schedule_a、schedule_b：上課時段，格式和 Course.schedule 相同

    回傳：
        重疊的時段，格式和 Course.schedule 相同，星期和節次都由小到大；沒有重疊時是 {}

    例子：
        find_conflicts({"2": [3, 4], "4": [5]}, {"2": [4, 5], "4": [5]}) → {"2": [4], "4": [5]}
        find_conflicts({"1": [1, 2]}, {"2": [1, 2]}) → {}

    對應需求：F2-01、F2-03
    """
    raise NotImplementedError
