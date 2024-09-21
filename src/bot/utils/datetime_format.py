
from datetime import datetime, timedelta


def datetime_from_string(s: str):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def datetime_to_string(d: datetime):
    return d.strftime("%Y-%m-%d %H:%M:%S")

def timedelta_from_string(s: str):
    return timedelta(seconds=int(s))