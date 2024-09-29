
from datetime import datetime, timedelta

def datetime_from_string(s: str):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")

def datetime_to_string(d: datetime):
    return d.strftime("%Y-%m-%d %H:%M:%S")

def timedelta_from_string(s: str):
    return timedelta(seconds=int(s))

def calculate_end_time_by_minutes(start_time: datetime, duration_minutes: int) -> datetime:
    end_time = start_time + timedelta(minutes=duration_minutes)
    return end_time

def calculate_end_time_by_days(start_time: datetime, duration_days: int) -> datetime:
    end_time = start_time + timedelta(days=float(duration_days))
    return end_time

