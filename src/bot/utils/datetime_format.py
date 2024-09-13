
import datetime


def datetime_from_string(s: str):
    return datetime.datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def datetime_to_string(d: datetime.datetime):
    return d.strftime("%Y-%m-%d %H:%M:%S")