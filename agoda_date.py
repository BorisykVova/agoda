from datetime import datetime, timedelta
from random import randint


def get_date(days: int = 0, day_range: int = 0) -> str:
    if day_range:
        days += randint(1, day_range)

    date = datetime.now() + timedelta(days=days)
    return datetime.strftime(date, "%Y-%m-%d")


def valid_date(date: str) -> str:
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
