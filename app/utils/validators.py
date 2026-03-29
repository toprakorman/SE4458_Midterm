from datetime import datetime


def parse_iso_datetime(value: str):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def parse_date_only(value: str):
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def is_positive_integer(value) -> bool:
    return isinstance(value, int) and value > 0