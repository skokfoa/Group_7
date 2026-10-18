"""
時間規則：節次轉換、星期和節次是否合法。
全系統共用，之後其他功能或是函數都呼叫這裡。
"""

# 節次文字照順序排，第 1 個是第 1 節，第 12 個是 c
PERIOD_TEXTS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c"]


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
    if text in PERIOD_TEXTS:
        return PERIOD_TEXTS.index(text) + 1
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
    return PERIOD_TEXTS[number - 1]


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
    return day in ["1", "2", "3", "4", "5", "6", "7"]


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
    return period in range(1, 13)
